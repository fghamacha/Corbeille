

Parallel Deployment with WLX

1. Introduction

Parallel deployment is a feature of the PF toolchain that allows multiple SAS Liberty applications to be deployed simultaneously on the same target server. This approach significantly reduces the overall deployment time compared to sequential deployment, where applications are deployed one after the other.

2. Requirements

a) WebSphere Liberty Base (WLB)

Parallel deployment is only compatible with WebSphere Liberty Base (WLB). It is not yet supported for WebSphere Liberty Core (WLC) or within the integration environment via Jenkins.

b) host_vars Configuration

The host_vars.yml file must include the is_true key. If this value is either absent or set to false (which is the default), sequential deployment will be triggered. Important: If this value differs between any of the SAS instances within the same deployment, the entire parallel deployment will fail.

c) Resource Considerations

Parallel deployment can be resource-intensive. It is strongly recommended to limit the number of SAS instances in a parallel deployment to 5, in order to avoid overloading the system.


---

Would you like any other sections added or any changes made?

