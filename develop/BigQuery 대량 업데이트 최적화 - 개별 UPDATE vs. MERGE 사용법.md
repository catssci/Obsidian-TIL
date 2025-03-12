BigQuery에서 데이터를 업데이트할 때 개별 `UPDATE` 방식을 사용하면 데이터가 많아질수록 속도가 크게 저하됩니다. 특히 수만 개 이상의 데이터를 한 번에 업데이트해야 하는 경우, BigQuery의 `MERGE` 문을 활용하면 훨씬 빠르고 효율적으로 처리할 수 있습니다.

이 글에서는 **개별 `UPDATE` 방식과 `MERGE` 방식의 차이점**을 알아보고, 성능 최적화를 위한 코드를 공유하겠습니다.

---

### 1. 개별 UPDATE 실행 방식 (비효율적인 방법)

이 방식은 각 행마다 하나의 쿼리를 실행하므로, 업데이트할 행이 많을수록 속도가 매우 느려집니다.

#### 📌 개별 UPDATE 코드 예시

```python
from google.cloud import bigquery

client = bigquery.Client()

table_full_path = "project.dataset.table"
update_df = ...  # 변경된 데이터가 담긴 DataFrame

if update_df.empty:
    print("업데이트할 데이터가 없습니다.")
else:
    for _, row in update_df.iterrows():
        query = f"""
        UPDATE `{table_full_path}`
        SET
            goods_price = @goods_price,
            sale_price = @sale_price,
            sale_percent = @sale_percent
        WHERE product_code = @product_code
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("goods_price", "FLOAT64", row["goods_price"]),
                bigquery.ScalarQueryParameter("sale_price", "FLOAT64", row["sale_price"]),
                bigquery.ScalarQueryParameter("sale_percent", "FLOAT64", row["sale_percent"]),
                bigquery.ScalarQueryParameter("product_code", "STRING", row["product_code"]),
            ]
        )

        query_job = client.query(query, job_config=job_config)
        query_job.result()

    print(f"{len(update_df)}개의 행이 업데이트되었습니다.")
```

#### ⚠ 문제점
- 행 개수만큼 쿼리를 실행하여 속도가 느림
- 데이터가 많아질수록 시간이 크게 증가
- BigQuery 비용이 증가함

---

### 2. MERGE 문을 활용한 대량 업데이트 (효율적인 방법)

BigQuery의 `MERGE` 문을 사용하면 한 번의 쿼리로 여러 개의 행을 빠르고 효율적으로 업데이트할 수 있습니다.

#### 📌 MERGE 코드 예시

```python
from google.cloud import bigquery

client = bigquery.Client()

table_full_path = "project.dataset.table"
temp_table = "project.dataset.temp_update_table"

if update_df.empty:
    print("업데이트할 데이터가 없습니다.")
else:
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    job = client.load_table_from_dataframe(update_df, temp_table, job_config=job_config)
    job.result()

    print(f"임시 테이블 `{temp_table}`에 {len(update_df)}개의 행을 로드했습니다.")

    query = f"""
    MERGE `{table_full_path}` AS target
    USING `{temp_table}` AS source
    ON target.product_code = source.product_code
    WHEN MATCHED THEN
    UPDATE SET
        target.goods_price = source.goods_price,
        target.sale_price = source.sale_price,
        target.sale_percent = source.sale_percent
    """

    query_job = client.query(query)
    query_job.result()

    print(f"{len(update_df)}개의 행이 한 번에 업데이트되었습니다!")
```

---

### ⚡ 개별 UPDATE vs. MERGE 성능 비교

| 방법 | 실행 속도 | 쿼리 실행 횟수 | 비용 |
|------|---------|--------------|------|
| 개별 UPDATE 실행 | ❌ 느림 | 행 개수만큼 실행 | ❌ 높음 |
| MERGE 사용 | ✅ 빠름 | 1회 실행 | ✅ 낮음 |

#### 📌 왜 MERGE가 더 빠를까?
- MERGE는 여러 행을 동시에 업데이트할 수 있기 때문입니다.
- 개별 UPDATE는 각 쿼리마다 별도의 작업을 생성하여 느립니다.
- BigQuery 비용도 MERGE 방식이 더 경제적입니다.

---

### 🎯 결론

- 개별 UPDATE 방식은 성능과 비용 면에서 비효율적입니다.
- MERGE 문을 사용하면 성능과 비용 모두 최적화할 수 있습니다.