Create Table gifts(
  id text NOT NULL UNIQUE,
  name text,
  tags text NOT NULL,
  meta text,
  created_at text NOT NULL,
  updated_at text NOT NULL,
  thumbnail_url text NOT NULL,
  points bigint NOT NULL,
  begins_at text NOT NULL,
  ends_at text NOT NULL
);
