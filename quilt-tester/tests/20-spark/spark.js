const {createDeployment, publicInternet, enough} = require('@quilt/quilt');
let spark = require('@quilt/spark');
let infrastructure = require('../../config/infrastructure.js');

// Application
// sprk.exclusive enforces that no two Spark containers should be on the same
// node. sprk.exposeUIToPublic says that the the public internet should be able
// to connect to the Spark web interface. sprk.job causes Spark to run that
// job when it boots.
const sprk = new spark.Spark(1, nWorker)
  .exclusive()
  .exposeUIToPublic()
  .job('run-example SparkPi');

let deployment = createDeployment({});
deployment.deploy(infrastructure);
deployment.deploy(sprk);

deployment.assert(publicInternet.canReach(sprk.masters), true);
deployment.assert(enough, true);
