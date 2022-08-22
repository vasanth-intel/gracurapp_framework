import os

FRAMEWORK_HOME_DIR = os.getcwd()
LOGS_DIR = FRAMEWORK_HOME_DIR + "/logs"
PERF_RESULTS_DIR = FRAMEWORK_HOME_DIR + "/results"

REPO_PATH             = os.path.join(os.getcwd(), "contrib_repo")
ORIG_CURATED_PATH     = os.path.join(os.getcwd(), "orig_contrib_repo")
CONTRIB_GIT_CMD       = "git clone -b gsc_image_curation https://github.com/veenasai2/contrib.git orig_contrib_repo"
#GIT_CHECKOUT_CMD      = "git checkout gsc_image_curation"
CURATED_PATH          = "Examples/gsc_image_curation"
CURATED_APPS_PATH     = os.path.join(REPO_PATH, CURATED_PATH)
VERIFIER_DOCKERFILE   = os.path.join(ORIG_CURATED_PATH, CURATED_PATH, "verifier_image/verifier.dockerfile")

HTTP_PROXY = "http://proxy-dmz.intel.com:911/"
HTTPS_PROXY = "http://proxy-dmz.intel.com:912/"
TEST_SLEEP_TIME_BW_ITERATIONS = 15
