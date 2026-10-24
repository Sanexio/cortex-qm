use cortex_app_core::{AppId, Klasse};

pub const APP_ID_STR: &str = "cortex-qm";
pub const PRODUKTNAME: &str = "Cortex QM";
pub const BUNDLE_ID: &str = "de.sanexio.cortex-qm";
pub const VERSION: &str = "0.1.0";
pub const KLASSE: Klasse = Klasse::K0;

pub fn app_id() -> AppId {
    AppId::neu(APP_ID_STR).expect("APP_ID Konstante ungueltig")
}
