import os

FRAMEWORK_HOME_DIR = os.getcwd()
#GRAMINE_HOME_DIR = FRAMEWORK_HOME_DIR + "/gramine"
LOGS_DIR = FRAMEWORK_HOME_DIR + "/logs"
PERF_RESULTS_DIR = FRAMEWORK_HOME_DIR + "/results"

#CURATED_APP_FRAMEWORK_HOME_DIR = os.path.join(FRAMEWORK_HOME_DIR, "curated_apps")
#GRAMERF_HOME_DIR = os.path.join(FRAMEWORK_HOME_DIR, "gramerf_framework")
REPO_PATH             = os.path.join(os.getcwd(), "contrib_repo")
ORIG_CURATED_PATH     = os.path.join(os.getcwd(), "orig_contrib_repo")
CONTRIB_GIT_CMD       = "git clone -b gsc_image_curation https://github.com/veenasai2/contrib.git orig_contrib_repo"
#GIT_CHECKOUT_CMD      = "git checkout gsc_image_curation"
CURATED_PATH          = "Examples/gsc_image_curation"
CURATED_APPS_PATH     = os.path.join(REPO_PATH, CURATED_PATH)
VERIFIER_DOCKERFILE   = os.path.join(ORIG_CURATED_PATH, CURATED_PATH, "verifier_image/verifier.dockerfile")

HTTP_PROXY = "http://proxy-dmz.intel.com:911/"
HTTPS_PROXY = "http://proxy-dmz.intel.com:912/"
SYSTEM_PACKAGES_FILE = "system_packages.yaml"
PYTHON_PACKAGES_FILE = "python_packages.yaml"
PKG_INSTALL_WAIT_TIME = 25
TEST_SLEEP_TIME_BW_ITERATIONS = 15
BUILD_TYPE = "release"
BUILD_PREFIX = FRAMEWORK_HOME_DIR + "/gramine_install/usr"

# Commands constants
#CURATED_APP_FRAMEWORK_CLONE_CMD = "git clone -b bprashan https://github.com/bprashan/curated_apps.git"

#GRAMERF_FRAMEWORK_CLONE_CMD = "git clone -b perf_gramine_tensorflow https://github.com/vasanth-intel/gramerf_framework.git"

#GRAMINE_CLONE_CMD = "git clone https://github.com/gramineproject/gramine.git"

EXAMPLES_REPO_CLONE_CMD = "git clone https://github.com/gramineproject/examples.git"

MIMALLOC_CLONE_CMD = "git clone -b v1.7.6 https://github.com/microsoft/mimalloc.git"

REDIS_DOWNLOAD_CMD = "wget https://github.com/antirez/redis/archive/6.0.5.tar.gz"

MIMALLOC_INSTALL_PATH = "/usr/local/lib/libmimalloc.so.1.7"

TCMALLOC_INSTALL_PATH = "/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"

BUILD_TYPE_PREFIX_STRING = "--prefix=" + BUILD_PREFIX + " --buildtype=" + BUILD_TYPE

GRAMINE_SGX_SED_CMD = "sed -i \"/uname/ a '/usr/src/linux-headers-@0@/arch/x86/include/uapi'.format(run_command('uname', '-r').stdout().split('-generic')[0].strip()),\" meson.build"

GRAMINE_BUILD_MESON_CMD = "meson setup build/ --werror " + \
                        BUILD_TYPE_PREFIX_STRING + \
                        " -Ddirect=enabled -Dsgx=enabled -Dtests=enabled > " + \
                        LOGS_DIR + "/gramine_build_meson_cmd_output.txt"

GRAMINE_NINJA_BUILD_CMD = "ninja -vC build > " + LOGS_DIR + "/gramine_ninja_build_cmd_output.txt"

GRAMINE_NINJA_INSTALL_CMD = "ninja -vC build install > " + LOGS_DIR + "/gramine_ninja_install_cmd_output.txt"

PYTHONPATH_CMD = "gramine/scripts/get-python-platlib.py " + BUILD_PREFIX

GRAMINE_SGX_GEN_PRIVATE_KEY_CMD = "gramine-sgx-gen-private-key -f"

APT_UPDATE_CMD = "sudo apt-get update"

APT_FIX_BROKEN_CMD = "sudo apt --fix-broken install -y"

SYS_PACKAGES_CMD = "sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y "

# Providing -H option to sudo to suppress the pip home directory warning.
# -U option is to install the latest package (if upgrade is available).
PYTHON_PACKAGES_CMD = "sudo -H python3 -m pip install -U "

PIP_UPGRADE_CMD = "python3 -m pip install --upgrade pip"

TENSORFLOW_INSTALL_CMD = "python3 -m pip install intel-tensorflow-avx512==2.4.0"

TF_BERT_INTEL_AI_MODELS_CLONE_CMD = "git clone https://github.com/IntelAI/models.git"

TF_BERT_DATASET_WGET_CMD = "wget https://storage.googleapis.com/bert_models/2019_05_30/wwm_uncased_L-24_H-1024_A-16.zip -P data/"
TF_BERT_DATASET_UNZIP_CMD = "unzip data/wwm_uncased_L-24_H-1024_A-16.zip -d data"
TF_BERT_SQUAAD_DATASET_WGET_CMD = "wget https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json -P data/wwm_uncased_L-24_H-1024_A-16"

TF_BERT_CHECKPOINTS_WGET_CMD = "wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/bert_large_checkpoints.zip -P data/"
TF_BERT_CHECKPOINTS_UNZIP_CMD = "unzip data/bert_large_checkpoints.zip -d data"
TF_BERT_FP32_MODEL_WGET_CMD = "wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v2_4_0/fp32_bert_squad.pb -P data/"

TF_RESNET_INTEL_AI_MODELS_CLONE_CMD = "git clone https://github.com/IntelAI/models.git"
TF_RESNET_INT8_MODEL_WGET_CMD = "wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/resnet50v1_5_int8_pretrained_model.pb"

LOG_LEVEL = "error"
