DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS eisen_intern;
CREATE TABLE "posts" (
	"id"	INTEGER,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"title"	TEXT NOT NULL,
	"content"	TEXT NOT NULL,
	"download_path"	TEXT,
	"display"	TEXT,
	"pic_data"	TEXT,
	"pic_name"	TEXT,
	"pic_comment"	TEXT,
	"pic_content_type"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "eisen_intern" (
	"id"	INTEGER NOT NULL,
	"browser_open"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);