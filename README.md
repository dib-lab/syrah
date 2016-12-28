# syrah!

syrah reads sequences from stdin and outputs subsequences containing solid
or trusted k-mers suitable for counting or MinHashing.

syrah automatically exits when it has seen enough solid k-mers.

## Options

You can specify the number of solid k-mers with `-n`.

You can set the k-mer size with `-k`.

There are no other options because options lead to anger. Anger leads to
hate. Hate leads to suffering.

## Use case

The primary use case for the moment is to extract a subset of solid
k-mers for loading into sourmash signatures.  For example,

    dump-fastq -A $SRA_ID -Z | syrah | sourmash compute - -o out.sig

will extract the first 1m solid k-mers from the given SRA data set and
feed them into `sourmash` to compute a signature.

CTB 12/2016
