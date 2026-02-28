> 分组规则

```json
{
  "generated_at": "2026-02-28 10:30:00",
  "total_features": 45,
  "common_features_count": 12,
  "unique_features_count": 33,
  "feature_groups": [
    {
      "group_id": "FG001",
      "type": "common",
      "feature_name": "唯一码验证",
      "modules": ["唯一码收货", "唯一码组盘"],
      "test_case_file": "0_用例复用.md",
      "aspects": {
        "common": ["空唯一码", "格式错误", "特殊字符"],
        "specific": {
          "唯一码收货": ["状态为初始化", "未绑定容器"],
          "唯一码组盘": ["容器未锁定"]
        }
      }
    }
  ]
}
```
