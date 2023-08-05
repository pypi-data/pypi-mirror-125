#include <nccl.h>
#include <pybind11/numpy.h>
#include <string>
#include <torch/extension.h>

namespace quiver
{

}

void register_cuda_quiver_comm(pybind11::module &m)
{
    // m.def("create_nccl_id", &quiver::create_nccl_id);
    // py::class_<quiver::NcclComm>(m, "NcclComm")
    //     .def(py::init<int, int, py::bytes>());
}