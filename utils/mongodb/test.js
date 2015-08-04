use admin
db.createUser(
  {
    user: "test",
    pwd: "test",
    roles: [
      { role: "userAdminAnyDatabase", db: "admin" },
      { role: "readWriteAnyDatabase", db: "admin" }, 
    ]
  }
)

use test
for (i = 0; i < 1000; i++) {
  db.users.insert({
    user_id : "user"+i,
    data: Math.floor(Math.random() * 100)
  })
}
