CREATE TABLE "User" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "email" varchar,
  "username" varchar,
  "password" varchar,
  "is_staff" bit
);
CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "title" varchar,
  "description" varchar,
  "post_image_url" varchar,
  "link" varchar,
  "timestamp" date,
  "platform_id" INTEGER,
  "game_id" INTEGER,
  "user_id" INTEGER,
  FOREIGN KEY(`platform_id`) REFERENCES `Platform`(`id`),
  FOREIGN KEY(`game_id`) REFERENCES `Game`(`id`) FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);
CREATE TABLE "Platforms" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "platform" varchar,
  "platform_image" varchar
);
CREATE TABLE "Games" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "title" varchar,
  "game_image_url" varchar,
  "platform_id" INTEGER,
  FOREIGN KEY(`platform_id`) REFERENCES `Platforms`(`id`)
);
CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);
CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);