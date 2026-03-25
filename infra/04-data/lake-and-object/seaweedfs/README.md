<!-- [ID:04-data:seaweedfs] -->
# SeaweedFS

> High-performance distributed file system and object storage.

## 1. Context & Objective

SeaweedFS is a fast, distributed storage system designed for storing and serving billions of files. In `hy-home.docker`, it provides a resilient and scalable storage layer for unstructured data, media, and logs, offering both Filer (filesystem) and S3 interfaces.

## 2. Requirements & Constraints

* **Architecture**: Uses a master-volume-filer architecture.
* **Resources**: `seaweedfs-master` and `seaweedfs-filer` use `template-stateful-med`, while `seaweedfs-volume` uses `template-stateful-high`.
* **Persistence**: Data is stored in `seaweedfs-master-data` and `seaweedfs-volume-data` volumes.
* **Network**: Service isolation on `infra_net`.

## 3. Setup & Installation

The stack consists of a Master, Volume, Filer, S3 interface, and a FUSE mount utility.

```bash
# Deploy SeaweedFS stack
docker compose up -d
```

| Service | Image | Role |
| :--- | :--- | :--- |
| `seaweedfs-master` | `chrislusf/seaweedfs:4.05` | Metadata Management |
| `seaweedfs-volume` | `chrislusf/seaweedfs:4.05` | Data Storage |
| `seaweedfs-filer` | `chrislusf/seaweedfs:4.05` | File System Interface |
| `seaweedfs-s3` | `chrislusf/seaweedfs:4.05` | S3 API Compatibility |
| `seaweedfs-mount` | `chrislusf/seaweedfs:4.05` | FUSE Mount Utility |

## 4. Usage & Integration

* **Master UI**: `https://seaweedfs.${DEFAULT_URL}` (Port 9333).
* **Filer API**: `https://cdn.${DEFAULT_URL}` (Port 8888).
* **S3 API**: `https://s3.${DEFAULT_URL}` (Port 8333).
* **FUSE Mount**: Accessible at `/mnt/seaweedfs` on the host.

Integration Example:

```bash
# Check cluster status
curl http://seaweedfs-master:9333/cluster/status
```

## 5. Maintenance & Safety

* **Health Checks**: Master, Volume, Filer, and S3 have automated health probes.
* **Mount Security**: `seaweedfs-mount` runs in privileged mode with `SYS_ADMIN` capability.
* **Data Safety**: Ensure master and volume volumes are backed up. Volume size limit is set to 1GB per volume file.
* **Monitoring**: Use the master status page to monitor volume distribution and replication.

---

## Documentation References

* [Storage Systems Guide](../../../docs/07.guides/04-data/04.storage-systems.md)
* [Backup Operations](../../../docs/08.operations/04-data/README.md)
* [Disaster Recovery](../../../docs/09.runbooks/04-data/README.md)
