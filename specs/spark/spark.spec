(import "machines")

(define Namespace "CHANGE_ME")
(define AdminACL (list "local"))

(define sparkWorkerCount 3)

(define MasterCount 1)
(define WorkerCount (+ 1 sparkWorkerCount))
(machines.Boot
  MasterCount
  WorkerCount
  (list (provider "AmazonSpot")
        (size "m4.large")
        (githubKey "ejj")))

(label "spark-master"
    (docker "quay.io/netsys/spark" "di-start-master.sh"))

(label "spark-worker" (makeList sparkWorkerCount
    (docker "quay.io/netsys/spark"
        "di-start-worker.sh" "spark://spark-master.di:7077")))

(label "spark-nodes" "spark-master" "spark-worker")

(placement "exclusive" "spark-nodes" "spark-nodes")

// Spark workers listen on random ports. Must open up everything.
(connect (list 1000 65535) "spark-master" "spark-worker")
(connect (list 1000 65535) "spark-worker" "spark-worker")

(connect 7077 "spark-worker" "spark-master")
