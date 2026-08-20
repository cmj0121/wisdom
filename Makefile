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
#
# All four run even after one fails -- a run that stops at the first failure
# hides the rest -- so the loop must say so itself: the last line of a failing
# run used to be the LAST script's success sentence. The count is derived from
# the loop rather than written twice, so adding a fifth check cannot leave the
# summary claiming four.
test:				# run the four repo checks (not the validator self-test)
	@failed=0; total=0; summary=""; \
	for script in test check-version-sync validate check-skill-spec; do \
		total=$$((total + 1)); \
		if bash "scripts/$$script"; then \
			summary="$$summary  \033[32mPASS\033[0m scripts/$$script\n"; \
		else \
			failed=$$((failed + 1)); \
			summary="$$summary  \033[31mFAIL\033[0m scripts/$$script\n"; \
		fi; \
	done; \
	printf '\n==> Summary\n'; \
	printf '%b' "$$summary"; \
	if [ $$failed -eq 0 ]; then \
		printf '==> All %d checks passed\n' "$$total"; \
		exit 0; \
	fi; \
	printf '==> %d of %d checks FAILED -- re-run with WISDOM_VERBOSE=1 for per-item detail\n' "$$failed" "$$total"; \
	exit 1

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
