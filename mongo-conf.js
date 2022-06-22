db.createUser({
    user: "test",
    pwd: "test",
    roles: [
            {
                role:"readWrite",
                db: "imaging-mongo-db"
            }
        ]
    }
)