SUBDIR :=

.PHONY: all clean test run build upgrade install help $(SUBDIR)

all: $(SUBDIR) 		# default action
	@[ -f .git/hooks/pre-commit ] || pre-commit install --install-hooks
	@git config commit.template .git-commit-template

clean: $(SUBDIR)	# clean-up environment
	@find . -name '*.sw[po]' -delete

test:				# run test
	@bash scripts/test

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
