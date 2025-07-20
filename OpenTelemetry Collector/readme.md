**Usage**
1. This will help us convert the OTLP protobuf-encoded body into a JSON body.
2. However, the protocol remains OTLP. We need to convert and obtain proper JSON to utilize it in the DT App.
3. Therefore, we will add another layer (JSONConverter) that will specifically convert OTLP to an HTTP JSON response.