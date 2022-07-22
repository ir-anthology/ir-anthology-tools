IRANTHOLOGY_PROD_DIR := /mnt/ceph/storage/data-in-production/ir-anthology/
IRANTHOLOGY_TMP_DIR := $(IRANTHOLOGY_PROD_DIR)tmp/
IRANTHOLOGY_BIB_FILE_LOCAL := $(IRANTHOLOGY_PROD_DIR)sources/ir-anthology.bib

IRANTHOLOGY_DATA_GIT := https://github.com/ir-anthology/ir-anthology-data/raw/master/
IRANTHOLOGY_BIB_FILE_GIT := $(IRANTHOLOGY_DATA_GIT)ir-anthology.bib

# TODO: SETUP VENV

.PHONY: all
all:
	@echo "Just here to catch an accidental make (all)!"

# = CLEAN ======================================================================

.PHONY: clean
clean: clean/delete-ir-anthology-bib

.PHONY: clean-tmp
clean-tmp: clean/delete-corpus-wcsp15
	ls -lAhF $(IRANTHOLOGY_PROD_DIR)tmp/

# SINGLE FILES

.PHONY: clean/delete-ir-anthology-bib
clean/delete-ir-anthology-bib:
	rm -f $(IRANTHOLOGY_BIB_FILE_LOCAL)

# tmp/ corpora cleanup

.PHONY: clean/delete-corpus-wcsp15
clean/delete-corpus-wcsp15:
	rm -rf $(IRANTHOLOGY_TMP_DIR)wcsp15/

# = DATA =======================================================================

.PHONY: data
data: data/download-ir-anthology-bib

.PHONY: data/download-ir-anthology-bib
data/download-ir-anthology-bib: clean/delete-ir-anthology-bib
	wget $(IRANTHOLOGY_BIB_FILE_GIT) -O $(IRANTHOLOGY_BIB_FILE_LOCAL)

.PHONY: data/papers-wanted
data/papers-wanted: data/download-ir-anthology-bib
	python3 scripts/generate_papers_wanted.py $(IRANTHOLOGY_PROD_DIR)sources/papers_wanted.json

.PHONY: data/papers-from-wcsp
data/papers-from-wcsp:
	@echo "This target expects an up-to-date papers_wanted.json - To update it, run >>make data/papers-wanted<<"
	@echo "This target expects a copy of the WSCP15 corpus - To create it, run >>make data/corpus-extract-wcsp15<<"
	@[ -f $(IRANTHOLOGY_PROD_DIR)sources/papers_wanted.json ] && echo "TODO WCSP INGEST" || echo "ERROR: papers_wanted.json does not exist!"

.PHONY: data/corpus-extract-wcsp15
data/corpus-extract-wcsp15: clean/delete-corpus-wcsp15
	mkdir -p $(IRANTHOLOGY_TMP_DIR)wcsp15/
	unzip /mnt/ceph/storage/corpora/corpora-webis/corpus-webis-csp-15/webis-csp-15-corpus.zip -d $(IRANTHOLOGY_TMP_DIR)wcsp15/ && \
		cp /mnt/ceph/storage/corpora/corpora-webis/corpus-webis-csp-15/webis-csp-15-metadata.ldjson $(IRANTHOLOGY_TMP_DIR)wcsp15/ && \
		cp /mnt/ceph/storage/corpora/corpora-webis/corpus-webis-csp-15/webis-csp-15-plaintext.ldjson $(IRANTHOLOGY_TMP_DIR)wcsp15/

# = DOWNLOAD ===================================================================

