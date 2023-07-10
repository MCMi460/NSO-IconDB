Create Table categories(
  key text NOT NULL UNIQUE,
  name text NOT NULL,
  image_url text NOT NULL,
  description text,
  key_color text NOT NULL
);
