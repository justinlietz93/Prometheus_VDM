
// Minimal HIP CSR SpMV placeholder (A*y = x) with pybind11 bindings.
// Replace with tuned Composable Kernel kernels as you iterate.
#include <hip/hip_runtime.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

__global__ void spmv_csr_kernel(
    const int N,
    const int* __restrict__ indptr,
    const int* __restrict__ indices,
    const float* __restrict__ data,
    const float* __restrict__ x,
    float* __restrict__ y
){
    int row = blockIdx.x * blockDim.x + threadIdx.x;
    if (row < N){
        float sum = 0.f;
        int start = indptr[row];
        int end   = indptr[row+1];
        for (int p=start; p<end; ++p){
            sum += data[p] * x[ indices[p] ];
        }
        y[row] = sum;
    }
}

py::array_t<float> spmv_csr(py::array_t<int> indptr,
                            py::array_t<int> indices,
                            py::array_t<float> data,
                            py::array_t<float> x){
    auto buf_indptr = indptr.request();
    auto buf_indices = indices.request();
    auto buf_data = data.request();
    auto buf_x = x.request();

    int N = buf_indptr.shape[0] - 1;
    auto y = py::array_t<float>(N);
    auto buf_y = y.request();

    // NOTE: This placeholder copies to device each call. For production,
    // allocate device buffers once and stream updates.
    int *d_indptr, *d_indices;
    float *d_data, *d_x, *d_y;
    hipMalloc(&d_indptr, buf_indptr.size * sizeof(int));
    hipMalloc(&d_indices, buf_indices.size * sizeof(int));
    hipMalloc(&d_data,   buf_data.size   * sizeof(float));
    hipMalloc(&d_x,      buf_x.size      * sizeof(float));
    hipMalloc(&d_y,      buf_y.size      * sizeof(float));

    hipMemcpy(d_indptr, buf_indptr.ptr, buf_indptr.size * sizeof(int), hipMemcpyHostToDevice);
    hipMemcpy(d_indices, buf_indices.ptr, buf_indices.size * sizeof(int), hipMemcpyHostToDevice);
    hipMemcpy(d_data, buf_data.ptr, buf_data.size * sizeof(float), hipMemcpyHostToDevice);
    hipMemcpy(d_x, buf_x.ptr, buf_x.size * sizeof(float), hipMemcpyHostToDevice);

    int threads = 256;
    int blocks = (N + threads - 1) / threads;
    hipLaunchKernelGGL(spmv_csr_kernel, dim3(blocks), dim3(threads), 0, 0, N, d_indptr, d_indices, d_data, d_x, d_y);
    hipDeviceSynchronize();

    hipMemcpy(buf_y.ptr, d_y, buf_y.size * sizeof(float), hipMemcpyDeviceToHost);
    hipFree(d_indptr); hipFree(d_indices); hipFree(d_data); hipFree(d_x); hipFree(d_y);
    return y;
}

PYBIND11_MODULE(fum_ck, m){
    m.doc() = "FUM HIP CSR SpMV (placeholder)";
    m.def("spmv_csr", &spmv_csr, "CSR SpMV via HIP");
}
