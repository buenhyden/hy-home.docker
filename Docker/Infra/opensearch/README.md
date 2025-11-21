# OpenSearch

**OpenSearch**는 Elasticsearch에서 파생된 오픈 소스 검색 및 분석 엔진입니다.
로그 분석, 실시간 애플리케이션 모니터링, 클릭스트림 분석 등에 사용됩니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **opensearch-node1** | 검색 엔진 노드 (Single Node) | `9200` |
| **opensearch-dashboards** | 데이터 시각화 (Kibana 포크) | `5601` |
| **opensearch-exporter** | Prometheus용 메트릭 Exporter | `9114` |

## 🛠 설정 및 환경 변수

- **모드**: 개발 편의를 위해 `discovery.type=single-node`로 설정되어 있습니다.
- **인증**: `OPENSEARCH_INITIAL_ADMIN_PASSWORD`로 관리자 비밀번호 설정.
- **Dashboards**: `http://localhost:5601` 접속.

## 📦 볼륨 마운트

- `opensearch-data1`: 데이터 저장소

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **메모리**: Java Heap 설정(`-Xms1g -Xmx1g`)과 시스템 `vm.max_map_count` 설정(262144 이상)이 필요할 수 있습니다.
