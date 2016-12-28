# syrah!

syrah reads sequences from stdin and outputs subsequences containing solid
or trusted k-mers suitable for counting or MinHashing.

syrah automatically exits when it has seen enough solid k-mers.

## Options

You can specify the number of solid k-mers with `-n`.

You can set the k-mer size with `-k`.

You can eliminate all output with `-q`.

There are no other options because options lead to anger. Anger leads to
hate. Hate leads to suffering.

## Use cases

The primary use case for the moment is to extract a subset of solid
k-mers for loading into sourmash signatures.  For example,

    dump-fastq -A $SRA_ID -Z | syrah | sourmash compute - -o out.sig

will extract the first 1m solid k-mers from the given SRA data set and
feed them into `sourmash` to compute a signature.  Once enough k-mers are
found, `syrah` will terminate the stream.

The default parameters are designed for small microbial genomes (where
1m k-mers is usually between 20-50% of the genome) and may be OK for
metagenome and transcriptome overlap analysis, but for other
situations you may need to vary `-n`.

CTB 12/2016
