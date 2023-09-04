# EzUA Tutorials

Welcome to the EzUA Tutorials repository! This is the official source for tutorials related to the EzUA analytics platform.
Whether you're a beginner or an advanced user, you'll find useful content to help you make the most out of EzUA's capabilities.

![ezua-tutorials](images/ezua-tutorials.jpg)

## Repository Structure

This repository is organized into two main directories:

- [Integration Tutorials](integration-tutorials): Tutorials that demonstrate how to integrate various applications
  like Kubeflow, Feast, Spark, and MLflow within the EzUA platform.
- [Applications](applications): Specialized tutorials tailored to specific real-world applications.

### Integration Tutorials

Navigate to the `integration-tutorials` directory to find a collection of tutorials that cover a wide array of topics in analytics
and data science. These tutorials are designed to help you grasp the foundational elements of working within EzUA.

### Application-Specific Tutorials

For tutorials that are tailored to specific applications, go to the `applications`` directory. You'll find specialized guides that show
you how to leverage EzUA's tools for particular use-cases. The current list of application-specific tutorials include:

- [FEAST feature store](applications/feast/): Ride sharing tutorial
- [Kubeflow Pipelines](applications/kubeflow-pipelines/): Financial time series tutorial
- [MLflow](applications/mlflow): Bike sharing tutorial
- [RAY](applications/ray): News recommendation tutorial

## Getting Started

1. Clone this repository:

    ```bash
    git clone https://github.com/HPEEzmeral/ezua-tutorials.git
    ```

2. Navigate to the desired directory.
3. Follow the README in the respective directory for further instructions.

## Requirements

These tutorials assume you have a basic understanding of Python programming and some familiarity with analytics and data science concepts.
Each tutorial may have additional specific requirements, which will be detailed within.

## Versioning

The tutorials in this repository are versioned to align with the releases of the EzUA platform. This ensures that the tutorials are compatible with the current capabilities and features of EzUA.

It is highly recommended to match the versions to avoid any discrepancies or issues. If you're using an older version of EzUA, be sure to check out the tutorials that are compatible with that specific version using the `tag` property of Git:

```bash
git checkout tags/release-x.x.x -b run-release-x.x.x
```

## License

This repository is licensed under the ... - see the LICENSE file for details.

## Support

If you need further assistance or have questions, consult our official [documentation](docs.ezmeral.hpe.com) or reach out through our support channels.