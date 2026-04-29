TASKS = [
    # CrashLoopBackOff / OOM
    {
        "id": "E01",
        "event": {
            "timestamp": "2025-01-15T10:23:01Z",
            "source": "kubelet",
            "pod": "api-gateway-7f8d9b",
            "namespace": "prod",
            "event_type": "CrashLoopBackOff",
            "details": {
                "restart_count": 5,
                "last_log": "panic: runtime error: invalid memory address",
                "reason": "OOMKilled",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") in ["critical", "high"]
            and resp.get("category") == "compute"
            and any(
                k in resp.get("action", "").lower()
                for k in ["diagnose", "escalate", "auto_fix"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in ["oom", "память", "memory", "лимит", "limit", "утечка"]
            )
        ),
    },
    {
        "id": "E02",
        "event": {
            "timestamp": "2025-01-15T11:05:22Z",
            "source": "kubelet",
            "pod": "payment-worker-8d7f2",
            "namespace": "payments",
            "event_type": "CrashLoopBackOff",
            "details": {
                "restart_count": 3,
                "last_log": "FATAL: out of memory (Needed 1.2GB, limit 512MB)",
                "memory_limit": "512Mi",
                "memory_request": "256Mi",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "critical"
            and resp.get("category") == "compute"
            and any(
                k in resp.get("action", "").lower() for k in ["auto_fix", "escalate"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "увеличить лимит",
                    "increase limit",
                    "1.2gb",
                    "не хватает",
                    "памяти",
                ]
            )
        ),
    },
    {
        "id": "E03",
        "event": {
            "timestamp": "2025-01-15T12:30:15Z",
            "source": "kubelet",
            "pod": "frontend-v2-9k3m4",
            "namespace": "prod",
            "event_type": "Failed",
            "details": {
                "reason": "LivenessProbeFailed",
                "message": "dial tcp 10.244.1.5:8080: connect: connection refused",
                "probe_config": {
                    "port": 8080,
                    "path": "/health",
                    "initialDelaySeconds": 30,
                },
            },
        },
        "validate": lambda resp: (
            resp.get("severity") in ["warning", "high"]
            and resp.get("category") in ["network", "config"]
            and any(k in resp.get("action", "").lower() for k in ["diagnose"])
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "подключение",
                    "порт",
                    "8080",
                    "liveness probe",
                    "connection refused",
                    "/health",
                ]
            )
        ),
    },
    {
        "id": "E04",
        "event": {
            "timestamp": "2025-01-15T13:45:00Z",
            "source": "kubelet",
            "pod": "postgres-0",
            "namespace": "database",
            "event_type": "FailedMount",
            "details": {
                "volume": "pg-data",
                "error": "data directory /var/lib/postgresql/data has wrong ownership",
                "current_owner": "root",
                "expected_owner": "999",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "critical"
            and resp.get("category") in ["storage", "config"]
            and any(k in resp.get("action", "").lower() for k in ["diagnose"])
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "ownership",
                    "владелец",
                    "владельц",
                    "права",
                    "fsgroup",
                    "chown",
                    "initcontainer",
                ]
            )
        ),
    },
    # Network / DNS
    {
        "id": "E05",
        "event": {
            "timestamp": "2025-01-15T14:10:33Z",
            "source": "network",
            "from_pod": "backend-7h4j2",
            "from_ns": "backend",
            "to_service": "frontend-svc",
            "to_ns": "frontend",
            "event_type": "ConnectionTimeout",
            "details": {
                "port": 8080,
                "ping_success": True,
                "curl_exit_code": 28,
                "duration_ms": 30000,
            },
        },
        "validate": lambda resp: (
            resp.get("severity") in ["warning"]
            and resp.get("category") == "network"
            and any(k in resp.get("action", "").lower() for k in ["diagnose"])
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "networkpolicy",
                    "selector",
                    "targetport",
                    "блокирует",
                    "сетев",
                    "маршрут",
                ]
            )
        ),
    },
    {
        "id": "E06",
        "event": {
            "timestamp": "2025-01-15T15:20:10Z",
            "source": "coredns",
            "event_type": "DNSTimeout",
            "details": {
                "pod": "worker-5f9d2",
                "namespace": "default",
                "query": "database-service.default.svc.cluster.local",
                "latency_ms": 5000,
                "coredns_pods": 2,
                "coredns_status": "running",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "warning"
            and resp.get("category") == "network"
            and any(
                k in resp.get("action", "").lower() for k in ["diagnose", "auto_fix"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in ["coredns", "реплики", "кэш", "ndots", "таймаут", "ожидан"]
            )
        ),
    },
    {
        "id": "E07",
        "event": {
            "timestamp": "2025-01-15T16:05:45Z",
            "source": "kube-proxy",
            "event_type": "NoEndpoints",
            "details": {
                "service": "payment-api",
                "namespace": "prod",
                "selector": "app=payment,env=prod",
                "matching_pods": 0,
            },
        },
        "validate": lambda resp: (
            resp.get("severity") in ["critical", "warning"]
            and resp.get("category") in ["network", "config"]
            and any(
                k in resp.get("action", "").lower() for k in ["escalate", "diagnose"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "selector не находит",
                    "endpoints",
                    "label mismatch",
                    "нет подов",
                    "селектор",
                ]
            )
        ),
    },
    # Node resources
    {
        "id": "E08",
        "event": {
            "timestamp": "2025-01-15T17:00:00Z",
            "source": "kubelet",
            "node": "worker-2",
            "event_type": "NodeCondition",
            "details": {
                "condition": "DiskPressure",
                "status": "True",
                "disk_usage_percent": 92,
                "image_volume_usage": "75GB",
                "available": "8GB",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") in ["warning", "critical"]
            and resp.get("category") == "storage"
            and any(
                k in resp.get("action", "").lower() for k in ["auto_fix", "diagnose"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "crictl rmi",
                    "образы",
                    "docker system prune",
                    "eviction",
                    "логи",
                    "диск",
                    "место",
                    "освобод",
                ]
            )
        ),
    },
    {
        "id": "E09",
        "event": {
            "timestamp": "2025-01-15T18:15:30Z",
            "source": "scheduler",
            "node": "worker-1",
            "event_type": "NodeCondition",
            "details": {
                "condition": "MemoryPressure",
                "status": "True",
                "allocatable_memory": "32GB",
                "capacity_memory": "64GB",
                "system_reserved": "16GB",
                "kube_reserved": "8GB",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "warning"
            and resp.get("category") == "compute"
            and any(k in resp.get("action", "").lower() for k in ["diagnose"])
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "system-reserved",
                    "allocatable",
                    "зарезервировано",
                    "eviction thresholds",
                    "память",
                ]
            )
        ),
    },
    {
        "id": "E10",
        "event": {
            "timestamp": "2025-01-15T19:30:00Z",
            "source": "scheduler",
            "event_type": "FailedScheduling",
            "details": {
                "pod": "new-app-6g7h3",
                "namespace": "staging",
                "pod_request": {"cpu": "2000m", "memory": "4Gi"},
                "node": "worker-3",
                "reason": "Insufficient memory",
                "node_available": "2Gi",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") in ["warning", "critical"]
            and resp.get("category") == "compute"
            and any(
                k in resp.get("action", "").lower() for k in ["escalate", "diagnose"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "не хватает памяти",
                    "request",
                    "limit",
                    "увеличить память",
                    "памяти",
                ]
            )
        ),
    },
    # Images / registry
    {
        "id": "E11",
        "event": {
            "timestamp": "2025-01-15T20:00:00Z",
            "source": "kubelet",
            "pod": "backend-9d8f2",
            "namespace": "prod",
            "event_type": "ImagePullBackOff",
            "details": {
                "image": "gitlab.example.com:5050/team/backend:v1.2.3",
                "error": "pull access denied, repository does not exist or may require authorization",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") in ["critical"]
            and resp.get("category") in ["config", "security"]
            and any(k in resp.get("action", "").lower() for k in ["escalate"])
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "imagepullsecret",
                    "secret",
                    "docker-registry",
                    "registry",
                    "доступ",
                    "права",
                    "разрешени",
                ]
            )
        ),
    },
    {
        "id": "E12",
        "event": {
            "timestamp": "2025-01-15T20:30:00Z",
            "source": "kubelet",
            "pod": "frontend-4h5j6",
            "namespace": "prod",
            "event_type": "ImagePullBackOff",
            "details": {
                "image": "nginx:latest",
                "error": "toomanyrequests: You have reached your pull rate limit",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "warning"
            and resp.get("category") == "config"
            and any(
                k in resp.get("action", "").lower() for k in ["auto_fix", "escalate"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "rate limit",
                    "docker hub",
                    "mirror",
                    "pull through cache",
                    "лимит",
                    "запросов",
                ]
            )
        ),
    },
    {
        "id": "E13",
        "event": {
            "timestamp": "2025-01-15T21:00:00Z",
            "source": "kubelet",
            "pod": "cron-worker-7k2m1",
            "namespace": "batch",
            "event_type": "ErrImageNeverPull",
            "details": {
                "image": "custom-app:v3",
                "pull_policy": "Never",
                "image_exists_on_node": False,
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "critical"
            and resp.get("category") == "config"
            and any(
                k in resp.get("action", "").lower() for k in ["diagnose", "auto_fix"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "imagepullpolicy never",
                    "образ отсутствует",
                    "always",
                    "ifnotpresent",
                    "образ",
                ]
            )
        ),
    },
    # PV / PVC
    {
        "id": "E14",
        "event": {
            "timestamp": "2025-01-15T22:00:00Z",
            "source": "persistentvolume-controller",
            "pvc": "data-pvc",
            "namespace": "database",
            "event_type": "PVCBoundFailed",
            "details": {
                "storage_class": "fast-ssd",
                "requested_size": "100Gi",
                "available_pvs": 0,
                "provisioner_status": "no provisioner found",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "critical"
            and resp.get("category") == "storage"
            and any(k in resp.get("action", "").lower() for k in ["escalate"])
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "provisioner",
                    "csi driver",
                    "не динамический",
                    "pv ручной",
                    "SCI",
                    "провайдер",
                    "storage class",
                ]
            )
        ),
    },
    {
        "id": "E15",
        "event": {
            "timestamp": "2025-01-15T22:45:00Z",
            "source": "kubelet",
            "pod": "mysql-1",
            "namespace": "data",
            "event_type": "FailedMount",
            "details": {
                "volume": "mysql-data",
                "error": "MountVolume.SetUp failed: volume mode 'Block' not supported by plugin 'kubernetes.io/hostpath'",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "warning"
            and resp.get("category") in ["storage", "config"]
            and any(k in resp.get("action", "").lower() for k in ["diagnose"])
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "volumemode block",
                    "filesystem",
                    "hostpath",
                    "изменить pvc",
                    "block",
                    "блоч",
                    "локаль",
                ]
            )
        ),
    },
    {
        "id": "E16",
        "event": {
            "timestamp": "2025-01-15T23:30:00Z",
            "source": "persistentvolume-controller",
            "event_type": "PVReleased",
            "details": {
                "pv_name": "pv-abc123",
                "old_claim": "data-pvc",
                "new_claim": None,
                "reclaim_policy": "Retain",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") in ["info", "warning"]
            and resp.get("category") == "storage"
            and any(k in resp.get("action", "").lower() for k in ["diagnose"])
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "released",
                    "claimref",
                    "удалить pv",
                    "reclaimpolicy delete",
                    "удал",
                    "очистка",
                    "освобож",
                ]
            )
        ),
    },
    # GitLab CI
    {
        "id": "E17",
        "event": {
            "timestamp": "2025-01-16T08:00:00Z",
            "source": "gitlab-runner",
            "pipeline_id": "12345",
            "job": "build",
            "event_type": "JobFailed",
            "details": {
                "error": "Cannot connect to the Docker daemon",
                "image": "docker:20",
                "runner_tags": ["docker", "linux"],
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "critical"
            and resp.get("category") == "compute"
            and any(k in resp.get("action", "").lower() for k in ["diagnose"])
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "docker",
                    "service",
                    "docker_host",
                    "privileged",
                    "kaniko",
                    "подключени",
                    "daemon",
                    "демон",
                    "сервис",
                ]
            )
        ),
    },
    {
        "id": "E18",
        "event": {
            "timestamp": "2025-01-16T09:15:00Z",
            "source": "gitlab-runner",
            "pipeline_id": "12346",
            "job": "test",
            "event_type": "JobFailed",
            "details": {
                "error": "no space left on device",
                "runner_type": "docker",
                "available_space": "500MB",
                "required_space_estimate": "2GB",
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "critical"
            and resp.get("category") in ["compute", "storage"]
            and any(
                k in resp.get("action", "").lower() for k in ["diagnose", "escalate"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "docker system prune",
                    "кэш",
                    "volume",
                    "clean",
                    "место",
                    "диск",
                ]
            )
        ),
    },
    # Security / RBAC
    {
        "id": "E19",
        "event": {
            "timestamp": "2025-01-16T10:00:00Z",
            "source": "kube-apiserver",
            "user": "john.doe",
            "namespace": "production",
            "event_type": "Forbidden",
            "details": {
                "action": "list pods",
                "error": "User cannot list resource pods in API group",
                "rbac_configured": False,
            },
        },
        "validate": lambda resp: (
            resp.get("severity") == "warning"
            and resp.get("category") in ["security", "config"]
            and any(
                k in resp.get("action", "").lower() for k in ["escalate", "diagnose"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "role",
                    "rolebinding",
                    "роль",
                    "namespace",
                    "kubectl create role",
                    "права",
                    "доступ",
                    "разрешени",
                    "RBAC",
                ]
            )
        ),
    },
    {
        "id": "E20",
        "event": {
            "timestamp": "2025-01-16T11:00:00Z",
            "source": "kube-apiserver",
            "service_account": "default",
            "source_ns": "team-a",
            "target_ns": "team-b",
            "event_type": "Audit",
            "details": {
                "action": "delete pod",
                "pod_name": "app-7d2f9",
                "verb": "delete",
                "allowed": True,
            },
        },
        "validate": lambda resp: (
            resp.get("severity") in ["info", "warning"]
            and resp.get("category") == "security"
            and any(
                k in resp.get("action", "").lower() for k in ["escalate", "diagnose"]
            )
            and any(
                k in resp.get("summary", "").lower()
                for k in [
                    "clusterrolebinding",
                    "слишком много прав",
                    "least privilege",
                    "service account scope",
                    "огранич",
                    "другом name",
                ]
            )
        ),
    },
]
