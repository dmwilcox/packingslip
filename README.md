# Packing Slip
Command line tools for quickly comparing files and directories. 

Ever need to know if a set of files was transfered correctly but are unable to
use rsync?  Maybe checksumming both sides will take too long, maybe the
filesystem was remote or removable.  Use packingslip!

Packingslip allows you to create _a packing slip_ just as in the world of
shipping with which you can verify that the contents are all present and
intact.  As a secondary benefit this allows you to verify integrity without
necessarily checksumming both sides -- since the checksums were recorded
during the packing slip creation.
