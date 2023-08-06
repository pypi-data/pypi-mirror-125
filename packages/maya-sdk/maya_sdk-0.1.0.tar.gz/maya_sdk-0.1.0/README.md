# maya-sdk
A client library for accessing Maya Insights API

## Usage

```python
import maya_sdk
maya_sdk.api_key = <API_KEY>
```

## API Key

Replace the <API_KEY> in the examples with an api key provided from Maya Insights. To generate a key, please contact our live chat support at https://mayainsights.com.

## Examples

### CSV Upload

```python
import maya_sdk
maya_sdk.api_key = <API_KEY>

with open("orders.csv", "rb") as f:
    maya_sdk.files.upload_csv(category="imported_orders", file=f)
```
