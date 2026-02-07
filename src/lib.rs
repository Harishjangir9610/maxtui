use pyo3::prelude::*;
pub mod py;
pub use py::*;

#[pymodule]
fn maxtui(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<py::App>()?;
    m.add_class::<py::Button>()?;
    m.add_class::<py::Input>()?;
    m.add_class::<py::Paragraph>()?;
    m.add_class::<py::Gauge>()?;
    m.add_class::<py::List>()?;
    m.add_class::<py::Table>()?;
    m.add_class::<py::Chart>()?;
    m.add_class::<py::Modal>()?;
    m.add_class::<py::Spinner>()?;
    m.add_class::<py::Color>()?;
    m.add_class::<py::Style>()?;
    m.add_class::<py::Theme>()?;
    m.add_class::<py::Layout>()?;
    m.add_class::<py::Constraint>()?;
    m.add_class::<py::TextAnimation>()?;
    m.add_class::<py::FrameAnimation>()?;
    m.add_class::<py::Effect>()?;
    m.add_class::<py::EffectManager>()?;
    
    m.add("__version__", "0.1.0")?;
    m.add("__doc__", "MaxTUI - High-Performance Terminal UI Framework")?;
    Ok(())
}
