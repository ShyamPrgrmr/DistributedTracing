# Database Setup

## Usage
```markdown
1. This section contains all the database configuration used in this project.  
Database: Mysql and redis
```

## How to exec it?
```sql
$ psql -U dt_user -d distributed_tracing -h localhost -p 5432
Password for user dt_user: password@123
psql (17.5)
Type "help" for help.

distributed_tracing=> select * from application_partition_mapping;
 id | application_id | partition_id | created_at | updated_at 
----+----------------+--------------+------------+------------
(0 rows)
```

