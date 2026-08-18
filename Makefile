SUBDIR :=

.PHONY: all clean test run build upgrade install help $(SUBDIR)

all: $(SUBDIR) 		# default action
	@[ -f .git/hooks/pre-commit ] || pre-commit install --install-hooks
	@git config commit.template .git-commit-template

clean: $(SUBDIR)	# clean-up environment
	@find . -name '*.sw[po]' -delete

# scripts/validate-fixtures is deliberately absent: it is the validator's own
# self-test rather than a check on this repo's contents, and it costs ~2.8s.
# pre-commit runs it whenever scripts/ changes.
test:				# run the three repo checks (not the validator self-test)
	@rc=0; \
	for script in test check-version-sync validate; do \
		bash "scripts/$$script" || rc=1; \
	done; \
	exit $$rc

run:				# run in the local environment

build:				# build the binary/library

install:			# symlink marketplace for /plugin usage
	@DEST="$$HOME/.claude/plugins/marketplaces/wisdom"; \
	if [ -d "$$DEST" ] && [ ! -L "$$DEST" ]; then \
		echo "WARNING: $$DEST exists and is not a symlink, skipping"; \
	else \
		mkdir -p "$$(dirname "$$DEST")"; \
		ln -sfn "$$(pwd)" "$$DEST"; \
		echo "Linked $$(pwd) -> $$DEST"; \
	fi

upgrade:			# upgrade all the necessary packages
	pre-commit autoupdate

help:				# show this message
	@printf "Usage: make [OPTION]\n"
	@printf "\n"
	@perl -nle 'print $$& if m{^[\w-]+:.*?#.*$$}' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?#"} {printf "    %-18s %s\n", $$1, $$2}'

$(SUBDIR):
	$(MAKE) -C $@ $(MAKECMDGOALS)
