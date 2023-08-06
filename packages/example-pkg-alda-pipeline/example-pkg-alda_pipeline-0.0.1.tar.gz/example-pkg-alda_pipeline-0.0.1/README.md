# AlDa Pipeline

Repository [here](https://gitlab.com/DanielSc4/alda-pipeline)

Setting up a CI/CD pipeline to automate development process using the Gitlab CI/CD infrastructure. 1st Assignment for Processo e sviluppo del software course @unimib

Students:
Daniel Scalena 844608
Alessandro Albi 817769

## What's has been done so far
We created ```.gtilab-ci.yml``` file where are definded all the stages and jobs listed in the Assignment file.

The project is a simple Python program using ```yfinance```, ```pandas``` and ```numpy``` as a requirement. It downloads, using Yahoo Finance APIs, the latest stock prices and volume order of Apple stock. A function able to compute returns (based on adj closes) is part of the front-end of the application.

Regarding the stages developed this is the current status:
| Stage            | Status                                                                                                           |
|------------------|------------------------------------------------------------------------------------------------------------------|
| **Build**            | :heavy_check_mark: This stage is currently working fine |
| **Verify**           | :heavy_check_mark: This stage is currently performing static and dynamic analysis correctly using ```Prospector``` and ```Bandit``` |
| **Unit test**        | :heavy_check_mark: This stage is currently working fine. Testing the Project's download and gets functions |
| **Integration test** | :heavy_check_mark: This stage is currently working fine. Testing the computation of Continuous compound returns |
| **Package**          | :heavy_check_mark: Stage is working and creating pkgs in ```./dist/``` folder |
| **Relase**           | :heavy_check_mark: This stage is currently working. Uploading the package to PiPy |
| **Deploy**           | This stage is currently under development |

