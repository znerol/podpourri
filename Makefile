ifeq ($(prefix),)
    prefix := /usr/local
endif
ifeq ($(exec_prefix),)
    exec_prefix := $(prefix)
endif
ifeq ($(bindir),)
    bindir := $(exec_prefix)/bin
endif
ifeq ($(libdir),)
    libdir := $(exec_prefix)/lib
endif
ifeq ($(systemddir),)
    systemddir := $(libdir)/systemd
endif
ifeq ($(systemduserdir),)
    systemduserdir := $(systemddir)/user
endif
ifeq ($(systemdsystemdir),)
    systemdsystemdir := $(systemddir)/system
endif
ifeq ($(datarootdir),)
    datarootdir := $(prefix)/share
endif
ifeq ($(mandir),)
    mandir := $(datarootdir)/man
endif
ifeq ($(python),)
    python := python
endif

all: bin test doc

man1 := $(patsubst doc/%.1.rst,doc/_build/man/%.1,$(wildcard doc/*.1.rst))
man1_installed := $(patsubst doc/_build/man/%,$(DESTDIR)$(mandir)/man1/%,$(man1))
man5 := $(patsubst doc/%.5.rst,doc/_build/man/%.5,$(wildcard doc/*.5.rst))
man5_installed := $(patsubst doc/_build/man/%,$(DESTDIR)$(mandir)/man5/%,$(man5))
man8 := $(patsubst doc/%.8.rst,doc/_build/man/%.8,$(wildcard doc/*.8.rst))
man8_installed := $(patsubst doc/_build/man/%,$(DESTDIR)$(mandir)/man8/%,$(man8))

scriptdirs := bin $(wildcard lib/*hooks)
scripts := $(foreach dir,$(scriptdirs),$(wildcard $(dir)/*))
scripts_installed := \
    $(patsubst bin/%,$(DESTDIR)$(bindir)/%,$(filter bin/%,$(scripts))) \
    $(patsubst lib/%,$(DESTDIR)$(libdir)/podpourri/%,$(filter lib/%,$(scripts)))

user_units := \
    $(wildcard lib/systemd/user/*.service) \
    $(wildcard lib/systemd/user/*.path) \
    $(wildcard lib/systemd/user/*.timer)
user_units_installed := \
    $(patsubst lib/systemd/user/%,$(DESTDIR)$(systemduserdir)/%,$(user_units))

user_dropindirs := \
    $(wildcard lib/systemd/user/*.service.d) \
    $(wildcard lib/systemd/user/*.path.d) \
    $(wildcard lib/systemd/user/*.timer.d)
user_dropindirs_installed := \
    $(patsubst lib/systemd/user/%,$(DESTDIR)$(systemduserdir)/%,$(user_dropindirs))

user_dropins := $(foreach dir,$(user_dropindirs),$(wildcard $(dir)/*.conf))
user_dropins_installed := \
    $(patsubst lib/systemd/user/%,$(DESTDIR)$(systemduserdir)/%,$(user_dropins))

system_units := \
    $(wildcard lib/systemd/system/*.service) \
    $(wildcard lib/systemd/system/*.path) \
    $(wildcard lib/systemd/system/*.timer)
system_units_installed := \
    $(patsubst lib/systemd/system/%,$(DESTDIR)$(systemdsystemdir)/%,$(system_units))

system_dropindirs := \
    $(wildcard lib/systemd/system/*.service.d) \
    $(wildcard lib/systemd/system/*.path.d) \
    $(wildcard lib/systemd/system/*.timer.d)
system_dropindirs_installed := \
    $(patsubst lib/systemd/system/%,$(DESTDIR)$(systemdsystemdir)/%,$(system_dropindirs))

system_dropins := $(foreach dir,$(system_dropindirs),$(wildcard $(dir)/*.conf))
system_dropins_installed := \
    $(patsubst lib/systemd/system/%,$(DESTDIR)$(systemdsystemdir)/%,$(system_dropins))

doc/_build/man/% : doc/%.rst
	${MAKE} -C doc man

bin: $(scripts)
	# empty for now

lint: bin
	shellcheck $(scripts)

test: bin
	PATH="$(shell pwd)/bin:${PATH}" $(python) -m test

doc: $(man1) $(man5) $(man8)

clean:
	${MAKE} -C doc clean
	-rm -rf dist
	-rm -rf build

# Install rule for executables/scripts
$(DESTDIR)$(bindir)/% : bin/%
	install -m 0755 -D $< $@

# Install rule for hook scripts
$(DESTDIR)$(libdir)/podpourri/% : lib/%
	install -m 0755 -D $< $@


# Install rule for systemd user units and dropins
$(DESTDIR)$(systemduserdir)/%: lib/systemd/user/%
	install -m 0644 -D $< $@

# Install rule for systemd system units and dropins
$(DESTDIR)$(systemdsystemdir)/%: lib/systemd/system/%
	install -m 0644 -D $< $@

# Install rule for manpages
$(DESTDIR)$(mandir)/man1/% : doc/_build/man/%
	install -m 0644 -D $< $@

# Install rule for manpages
$(DESTDIR)$(mandir)/man5/% : doc/_build/man/%
	install -m 0644 -D $< $@

# Install rule for manpages
$(DESTDIR)$(mandir)/man8/% : doc/_build/man/%
	install -m 0644 -D $< $@

install-doc: doc $(man1_installed) $(man5_installed) $(man8_installed)
	ln -s -f podpourri-build@.service.8 $(DESTDIR)$(mandir)/man8/podpourri-build-daily@.service.8
	ln -s -f podpourri-build@.service.8 $(DESTDIR)$(mandir)/man8/podpourri-build-weekly@.service.8
	ln -s -f podpourri-build@.service.8 $(DESTDIR)$(mandir)/man8/podpourri-build-daily@.timer.8
	ln -s -f podpourri-build@.service.8 $(DESTDIR)$(mandir)/man8/podpourri-build-weekly@.timer.8

install-bin: bin $(scripts_installed) $(entrypoints_installed) $(user_units_installed) $(user_dropins_installed) $(system_units_installed) $(system_dropins_installed)
	install -m 0644 lib/systemd/podpourri-build@.service $(DESTDIR)$(systemduserdir)/podpourri-build-daily@.service
	install -m 0644 lib/systemd/podpourri-build@.service $(DESTDIR)$(systemduserdir)/podpourri-build-weekly@.service
	install -m 0644 lib/systemd/podpourri-build@.service $(DESTDIR)$(systemdsystemdir)/podpourri-build-daily@.service
	install -m 0644 lib/systemd/podpourri-build@.service $(DESTDIR)$(systemdsystemdir)/podpourri-build-weekly@.service

install: install-bin install-doc

uninstall:
	-rm -f $(man1_installed)
	-rm -f $(man5_installed)
	-rm -f $(man8_installed)
	-rm -f $(scripts_installed)
	-rm -f $(entrypoints_installed)
	-rm -f $(user_units_installed)
	-rm -f $(user_dropins_installed)
	-rmdir $(user_dropindirs_installed)
	-rm -f $(system_units_installed)
	-rm -f $(system_dropins_installed)
	-rmdir $(system_dropindirs_installed)
	-rm -f $(DESTDIR)$(systemduserdir)/podpourri-build-daily@.service
	-rm -f $(DESTDIR)$(systemduserdir)/podpourri-build-weekly@.service
	-rm -f $(DESTDIR)$(systemdsystemdir)/podpourri-build-daily@.service
	-rm -f $(DESTDIR)$(systemdsystemdir)/podpourri-build-weekly@.service
	-rm -f $(DESTDIR)$(mandir)/man8/podpourri-build-daily@.service.8
	-rm -f $(DESTDIR)$(mandir)/man8/podpourri-build-weekly@.service.8
	-rm -f $(DESTDIR)$(mandir)/man8/podpourri-build-daily@.timer.8
	-rm -f $(DESTDIR)$(mandir)/man8/podpourri-build-weekly@.timer.8
	-rm -f $(DESTDIR)$(libdir)/podpourri/git-hooks/post-receive
	-rmdir $(DESTDIR)$(libdir)/podpourri/git-hooks
	-rmdir $(DESTDIR)$(libdir)/podpourri

dist-bin:
	-rm -rf build
	${MAKE} DESTDIR=build prefix=/ install
	mkdir -p dist
	tar --owner=root:0 --group=root:0 -czf dist/podpourri-dist.tar.gz -C build .

dist-src:
	mkdir -p dist
	git archive -o dist/podpourri-src.tar.gz HEAD

dist: dist-src dist-bin
	cd dist && md5sum podpourri-*.tar.gz > md5sum.txt
	cd dist && sha1sum podpourri-*.tar.gz > sha1sum.txt
	cd dist && sha256sum podpourri-*.tar.gz > sha256sum.txt

.PHONY: \
	all \
	clean \
	dist \
	dist-bin \
	dist-src \
	install \
	install-bin \
	install-doc \
	lint \
	test \
	uninstall \
