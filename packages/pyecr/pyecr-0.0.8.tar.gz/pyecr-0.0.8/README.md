**PyECR**
---
---

Command line tool that helps handle interactively the workflow of pushing images to AWS ECR. 

- Create or choose an AWS ECR Repository
- Pull an docker image to your local Docker
- Tag your docker image preparing it to upload to ECR
- Push the tagged docker image to ECR

```bash
# To run it, just call it...
$ pyecr
```


---

### **Troubleshooting**

#### **Error**:
```bash
TypeError: load_config() got an unexpected keyword argument 'config_dict'
```
#### **Solution**:

```bash
pip uninstall docker-compose
pip uninstall docker-py
pip uninstall docker-compose
pip install --upgrade --force-reinstall --no-cache-dir docker-compose
```