# SeaweedFS

## 📋 서비스 개요

SeaweedFS는 수십억 개의 파일을 저장하고 빠르게 제공할 수 있는 고성능 분산 파일 시스템 및 오브젝트 스토리지입니다. S3 호환 API를 제공하며, MinIO의 대안으로 사용할 수 있습니다.

### 주요 특징

- **S3 호환 API**: AWS S3와 호환되는 RESTful API 제공
- **고성능**: 메모리 기반 인덱싱으로 빠른 파일 액세스
- **확장성**: 마스터-볼륨-파일러 아키텍처로 수평 확장 가능
- **CDN 기능**: Filer를 통한 정적 파일 제공 최적화
- **FUSE 마운트**: 파일 시스템처럼 직접 마운트 가능
- **JWT 인증**: 내부 통신 보안 및 S3 API 인증

### 시스템 아키텍처에서의 역할

- **오브젝트 스토리지**: 애플리케이션의 대용량 파일 저장소
- **CDN 백엔드**: 정적 에셋(이미지, 비디오 등) 제공
- **백업 스토리지**: 로그, 트레이스 데이터 장기 보관 (Tempo, Loki)
- **미디어 스토리지**: 사용자 업로드 파일 관리

## 🏗️ 아키텍처

SeaweedFS는 다음 4개의 주요 컴포넌트로 구성됩니다:

```text
┌─────────────────┐
│   S3 Gateway    │ ← S3 API 엔드포인트 (s3.domain.com)
└────────┬────────┘
         │
┌────────▼────────┐
│     Filer       │ ← 파일 시스템 인터페이스 (cdn.domain.com)
└────────┬────────┘
         │
    ┌────▼────┐
    │ Master  │ ← 메타데이터 관리 (seaweedfs.domain.com)
    └────┬────┘
         │
    ┌────▼────┐
    │ Volume  │ ← 실제 데이터 저장
    └─────────┘
```

### 컴포넌트 설명

1. **Master**: 볼륨 할당 및 메타데이터 관리
2. **Volume**: 실제 파일 데이터 저장 (최대 10,000개 파일)
3. **Filer**: 파일 시스템 인터페이스 제공
4. **S3 Gateway**: S3 호환 API 제공
5. **Mount**: FUSE 마운트 지원 (선택사항)

## 🚀 설정 및 실행

### 환경 변수

`.env` 파일에서 다음 변수를 설정해야 합니다:

```env
# SeaweedFS Ports
SEAWEEDFS_MASTER_HTTP_PORT=9333
SEAWEEDFS_MASTER_GRPC_PORT=19333
SEAWEEDFS_VOLUME_HTTP_PORT=8080
SEAWEEDFS_VOLUME_GRPC_PORT=18080
SEAWEEDFS_FILER_HTTP_PORT=8888
SEAWEEDFS_FILER_GRPC_PORT=18888
SEAWEEDFS_S3_HTTP_PORT=8333

# Domain
DEFAULT_URL=yourdomain.com
```

### 보안 설정

`security.toml` 파일에서 다음을 설정합니다:

```toml
# JWT 서명 키 (내부 통신 암호화)
[jwt.signing]
key = "YourRandomSecretKey"
read.key = "YourRandomSecretKey"

# S3 액세스 계정
[aws.access.admin]
key = "minioadmin"              # Access Key ID
secret = "minioadminpassword"   # Secret Access Key
actions = ["Admin", "Read", "Write", "List", "Tagging"]
```

> [!WARNING]
> 프로덕션 환경에서는 반드시 강력한 비밀 키로 변경하세요!

### 실행 방법

```bash
# 전체 스택 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 특정 서비스만 시작
docker-compose up -d seaweedfs-master seaweedfs-volume seaweedfs-filer

# 중지
docker-compose down

# 데이터 포함 완전 삭제
docker-compose down -v
```

## 🔌 서비스 접근

### 웹 UI

Traefik을 통해 다음 도메인으로 접근 가능합니다:

- **Master UI**: `https://seaweedfs.yourdomain.com`
  - 클러스터 상태, 볼륨 정보 확인
- **Filer (CDN)**: `https://cdn.yourdomain.com`
  - 파일 시스템처럼 브라우저에서 접근
- **S3 API**: `https://s3.yourdomain.com`
  - S3 호환 클라이언트에서 사용

### S3 API 사용 예시

#### AWS CLI 설정

```bash
# AWS CLI 설정
aws configure --profile seaweedfs
# Access Key: minioadmin
# Secret Key: minioadminpassword
# Region: us-east-1
# Output: json

# 엔드포인트 URL 지정
export AWS_ENDPOINT=https://s3.yourdomain.com
```

#### 버킷 생성 및 사용

```bash
# 버킷 생성
aws --profile seaweedfs --endpoint-url=$AWS_ENDPOINT s3 mb s3://my-bucket

# 파일 업로드
aws --profile seaweedfs --endpoint-url=$AWS_ENDPOINT s3 cp file.txt s3://my-bucket/

# 파일 다운로드
aws --profile seaweedfs --endpoint-url=$AWS_ENDPOINT s3 cp s3://my-bucket/file.txt ./

# 버킷 목록
aws --profile seaweedfs --endpoint-url=$AWS_ENDPOINT s3 ls
```

#### Python (boto3) 예시

```python
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='https://s3.yourdomain.com',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadminpassword',
    region_name='us-east-1'
)

# 버킷 생성
s3.create_bucket(Bucket='my-bucket')

# 파일 업로드
s3.upload_file('local_file.txt', 'my-bucket', 'remote_file.txt')

# 파일 다운로드
s3.download_file('my-bucket', 'remote_file.txt', 'downloaded_file.txt')
```

### Filer API 사용 예시

```bash
# 파일 업로드
curl -F "file=@myfile.txt" https://cdn.yourdomain.com/path/to/upload/

# 파일 다운로드
curl https://cdn.yourdomain.com/path/to/file.txt -o file.txt

# 디렉토리 목록
curl https://cdn.yourdomain.com/path/to/folder/
```

## 📊 모니터링

### 헬스 체크

```bash
# Master 상태
curl http://localhost:9333/cluster/status

# Volume 상태
curl http://localhost:8080/status

# Filer 상태
curl http://localhost:8888/
```

### 주요 메트릭

각 컴포넌트는 자체 HTTP 포트에서 기본 상태 정보를 제공합니다:

- Master: 클러스터 토폴로지, 볼륨 할당 정보
- Volume: 디스크 사용량, 파일 개수
- Filer: 파일 시스템 통계

## 🗃️ 볼륨 및 데이터

### 영구 볼륨

```yaml
volumes:
  seaweedfs-master-data: # 클러스터 메타데이터
  seaweedfs-volume-data: # 실제 파일 데이터
```

### 백업 권장사항

- **Master 데이터**: 정기적으로 백업 (클러스터 복구에 필수)
- **Volume 데이터**: 중요 파일은 별도 백업 또는 복제 설정

## 🔧 성능 최적화

### 볼륨 설정

- `volumeSizeLimitMB=1024`: 각 볼륨의 최대 크기 (조정 가능)
- `max=10000`: 각 볼륨당 최대 파일 수 (조정 가능)
- `preStopSeconds=1`: 종료 전 대기 시간

### 캐싱

Mount 서비스의 캐싱 설정:

- `cacheCapacityMB=100`: 로컬 캐시 크기
- `concurrentWriters=128`: 동시 쓰기 스레드 수

### 확장 전략

1. **Volume 서버 추가**: 데이터 저장 용량 확장
2. **Master 복제**: 고가용성 확보 (3-5개 권장)
3. **Filer 복제**: 읽기 성능 향상

## 🔒 보안 고려사항

### 인증 및 권한

- JWT를 통한 내부 컴포넌트 간 인증
- S3 API는 액세스 키/시크릿 키 인증
- `security.toml`에서 여러 사용자 계정 정의 가능

### 네트워크 보안

- Traefik을 통한 TLS 종료
- 내부 네트워크(`infra_net`)로 격리
- 외부 포트 노출 최소화 (Traefik만 노출)

## 🐛 트러블슈팅

### "No free volumes" 오류

볼륨이 가득 찬 경우:

1. Volume 서버를 더 추가하거나
2. `volumeSizeLimitMB` 값을 늘리거나
3. 기존 파일 정리

### Filer 접근 불가

```bash
# Filer가 Master를 찾을 수 있는지 확인
docker logs seaweedfs-filer

# Master가 정상 작동 중인지 확인
docker logs seaweedfs-master
```

### S3 API 인증 실패

`security.toml` 파일이 제대로 마운트되었는지 확인:

```bash
docker exec seaweedfs-s3 cat /etc/seaweedfs/security.toml
```

## 📚 참고 자료

- [공식 문서](https://github.com/seaweedfs/seaweedfs/wiki)
- [S3 API 가이드](https://github.com/seaweedfs/seaweedfs/wiki/Amazon-S3-API)
- [Filer 설정](https://github.com/seaweedfs/seaweedfs/wiki/Filer-Setup)
- [보안 설정](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration)

## 🔗 관련 서비스

- **MinIO**: 또 다른 S3 호환 오브젝트 스토리지 (대안)
- **Traefik**: 리버스 프록시 및 TLS 종료
- **Tempo**: 트레이스 데이터 장기 보관에 SeaweedFS 사용 가능
- **Loki**: 로그 데이터 장기 보관에 SeaweedFS 사용 가능

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Master + Volume + Filer + S3 Gateway stack. |
| `config/` | `security.toml` and other config files. |
| `README.md` | Architecture, usage, and troubleshooting guide. |

## Documentation References

- **SeaweedFS Context Guide**: [docs/guides/04-data/seaweedfs-context.md](../../../docs/guides/04-data/seaweedfs-context.md)
