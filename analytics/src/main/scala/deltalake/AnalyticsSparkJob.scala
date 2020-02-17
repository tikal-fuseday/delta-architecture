package deltalake

import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import io.delta.tables._
import org.apache.spark.SparkConf


object AnalyticsSparkJob {
  def main(args: Array[String]): Unit = {

    val conf = new SparkConf()
      .setMaster("local[2]")
      .set("fs.s3.awsAccessKeyId", sys.props("AWS_ACCESS_KEY_ID"))
      .set("fs.s3.awsSecretAccessKey", sys.props("AWS_SECRET_ACCESS_KEY"))
    //    val conf = new SparkConf().setMaster("local[2]").set("fs.s3.access.key", sys.props("AWS_ACCESS_KEY_ID")).set("fs.s3.secret.key", sys.props("AWS_SECRET_ACCESS_KEY"))

    val deltaLakeInputPath = "s3a://delta-data.fuze/voter/silver/"
    val deltaLakeOutputPath = "s3a://delta-data.fuze/voter/gold"
    val spark = SparkSession.builder
      .config(conf)
      .appName("Spark SQL basic example")
      .getOrCreate()

    spark.sparkContext.hadoopConfiguration.set("fs.s3a.access.key",sys.props("AWS_ACCESS_KEY_ID"))
    spark.sparkContext.hadoopConfiguration.set("fs.s3a.secret.key",sys.props("AWS_SECRET_ACCESS_KEY"))

    import spark.implicits._
    val deltaTable = DeltaTable.forPath(spark, deltaLakeInputPath)
    val fullHistoryDf = deltaTable.history()
    printDf("fullHistoryDf", fullHistoryDf)
    val allVersions = fullHistoryDf.select($"version").collect()
    for (version <- allVersions) {
      val versionedDf = spark.read.format("delta").option("versionAsOf", version.get(0).toString).load(deltaLakeInputPath)
      versionedDf.show(false)
      //      versionedDf.write.partitionBy("pollId").mode(SaveMode.Append).save(deltaLakeOutputPath)


      DeltaTable.forPath(spark, deltaLakeOutputPath)
        .as("gold")
        .merge(
          versionedDf.as("updates"),
          "gold.pollId = updates.pollId and gold.voterId = updates.voterId and gold.ts < updates.ts")
        .whenMatched
        .updateExpr(
          Map("vote" -> "updates.vote"))
        .whenNotMatched
        .insertExpr(
          Map(
            "pollId" -> "updates.pollId",
            "voterId" -> "updates.voterId",
            "ts" -> "updates.ts",
            "vote" -> "updates.vote"))
        .execute()
    }
  }

  private def printDf(dfName: String, df: DataFrame, printSchema: Boolean = false): Unit = {
    println(s"$dfName's df")
    df.show(false)
    if (printSchema) {
      println(s"$dfName's schema:")
      df.printSchema()
    }
  }

}
