FROM konstin2/maturin

COPY Cargo.toml Cargo.lock ./
COPY fairvote/ fairvote/
COPY fairvote-py/ fairvote-py/

ENTRYPOINT [ "maturin" ]
CMD ["publish", "--manifest-path", "fairvote-py/Cargo.toml"]
