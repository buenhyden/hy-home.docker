# Pyroscope System Guide

> Continuous profiling and performance analysis.

---

## Overview (KR)

이 문서는 Pyroscope에 대한 가이드다. Pyroscope는 애플리케이션의 런타임 성능 데이터(CPU 사용량, 메모리 할당 등)를 지속적으로 수집(Continuous Profiling)하여 시각화한다. 이를 통해 성능 병목 지점, 데드락, 메모리 누수 등을 플레임그래프(Flamegraph)를 통해 직관적으로 분석할 수 있다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- SRE / DevOps
- Agent-tuner

## Purpose

Pyroscope의 핵심 기능인 지속적 프로파일링의 원리를 이해하고, Grafana와 연동하여 성능 문제를 분석하는 방법을 익힌다.

## Prerequisites

- [Grafana Alloy](../alloy.md) 프로파일링 수집 설정 완료
- [Grafana](../grafana.md) Pyroscope 데이터 소스 연결

## Step-by-step Instructions

### 1. 프로파일링 데이터 확인 (Exploration)

Grafana의 `Explore` 메뉴에서 `Pyroscope` 데이터 소스를 선택한다. `Application` 레이블을 필터링하여 특정 서비스의 최근 프로파일 데이터를 조회할 수 있다.

### 2. 플레임그래프(Flamegraph) 분석

- **CPU Profile**: 어떤 함수가 CPU 시간을 가장 많이 점유하고 있는지 확인한다. 넓은 bar는 해당 함수의 자체 실행 시간(Self Time) 또는 하위 호출 시간(Total Time)이 길다는 것을 의미한다.
- **Memory Profile**: 객체 할당(Allocations) 및 현재 점유 중인 메모리(In-use)를 분석하여 메모리 누수를 추적한다.

### 3. 시간대 비교 (Diff View)

성능 저하가 발생하기 전과 후의 프로파일을 비교하여 변경된 코드 경로를 식별한다.

### 4. 분산 추적 연동 (Trace-to-Profile)

Tempro와 연동되어 있는 경우, 특정 Trace ID와 관련된 프로파일을 바로 확인하여 요청 단위의 성능 병목을 수직적으로 분석할 수 있다.

## Common Pitfalls

- **오버헤드 (Overhead)**: 프로파일링 수집 빈도가 너무 높으면 애플리케이션 성능에 영향을 줄 수 있다. 기본 수집 주기를 유지하고 필요한 경우에만 조정하라.
- **레이블 카디널리티 (Label Cardinality)**: 너무 많은 고유 레이블(예: Request ID)을 프로파일에 추가하면 Pyroscope의 인덱싱 부하가 급증한다.
- **언어별 지원 차이**: Go, Java, Python, Rust 등 언어마다 수집 가능한 프로파일 종류(CPU, Mem, Block, Goroutine 등)가 다르므로 지원 범위를 확인하라.

## Related Documents

- **Infrastructure**: `[infra/06-observability/pyroscope/README.md](../../../infra/06-observability/pyroscope/README.md)`
- **Operation**: `[../08.operations/06-observability/pyroscope.md](../../08.operations/06-observability/pyroscope.md)`
- **Runbook**: `[../09.runbooks/06-observability/pyroscope.md](../../09.runbooks/06-observability/pyroscope.md)`
