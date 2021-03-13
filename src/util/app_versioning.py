# Application Version Number
# -------------------------------
# Release . Major . Minor . Patch
# -------------------------------
# Release - [Internal, Alpha, Beta, Release]
#            Interal - A build for internal use from developers only
#            Alpha - A build given to a select group for testing
#            Beta - A build given to the mass audience for testing
#            Release - A trusted build that can be given to any client
__release_type_internal__ = 'Internal'
__release_type_alpha__ = 'Alpha'
__release_type_beta__ = 'Beta'
__release_type_release__ = 'Release'

# Release - Indicates the broadest category to which this versioning belongs.  Explanations above.
__release_type__ = __release_type__internal
# Major - Indicates a fundamental change in how the application works
__release_num_major__ = '0'
# Minor - Indicates a new release to the public, a group of patches applied/features added
__release_num_minor__ = '0'
# Patch - An update that feels meaningful
__release_num_patch__ = '1'

app_version = __release_type__ + '.' + __release_num_major__ + '.' + __release_num_minor__ + '.' + __release_num_patch__