SUBDIR :=

.PHONY: all clean test eval doctor run build upgrade install help $(SUBDIR)

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

# Deliberately NOT part of `test`, for `doctor`'s reason and then some: every
# case here is a full Claude child session on the operator's own credential, so
# it wants a network and real money where the four checks want neither. CI is
# not an option either -- .github/workflows/checks.yml runs with
# `permissions: contents: read` and no secrets, and adding one to a public repo
# to automate a check a human can run by hand is a bad trade.
#
# --ablation none is not a speed knob. Under the default with-without ablation
# the CLI demotes a `tool_used: Skill` grader to a with-only indicator and stops
# scoring it -- and that grader is the only thing these cases assert.
# --no-publish keeps the HTML report off claude.ai, because a check in this repo
# uploading its results is a surprise nobody asked for.
#
# The CLI takes one plugin per invocation, so the list is derived from the cases
# on disk rather than written out: a case added under a new plugin needs no edit
# here, and a plugin with no cases is never invoked. The ceiling is therefore
# per plugin -- the largest set today is 4 cases x 3 runs, about $1.70 at the
# measured $0.142 a run, and all 13 cases together come to roughly $5.50.
#
# Like `test`, it runs every plugin even after one fails and fails at the end:
# a routing regression in the first plugin is no reason to leave the other
# eight unmeasured once the money is already committed.
eval:				# run the committed trigger cases (needs a credential, a network and ~$5.50)
	@failed=0; \
	for plugin in $$(find plugins -path '*/evals/*/prompt.md' | cut -d/ -f1-2 | sort -u); do \
		printf '\n==> %s\n' "$$plugin"; \
		claude plugin eval "$$plugin" \
			--trust-plugin \
			--ablation none \
			--no-publish \
			--max-cost-usd 3.00 || failed=$$((failed + 1)); \
	done; \
	if [ $$failed -ne 0 ]; then \
		printf '\n==> %d plugin suite(s) FAILED\n' "$$failed"; \
		exit 1; \
	fi

# Deliberately NOT part of `test`: this one asserts on the machine, not on the
# repo. There is no $$HOME/.claude in CI, where it would pass for the wrong
# reason, and a contributor's own skills are not this repo's business.
doctor:				# check the local machine for skills shadowing this marketplace
	@bash scripts/check-install-drift

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
