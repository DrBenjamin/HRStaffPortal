# Changelog

## [0.2.1](https://github.com/DrBenjamin/HRStaffPortal) - 2023-02-27

``` Version 0.2 Release```

### Added

* HR Staff Portal
    * Check for invited employees in Trainings to show in `multiselect` for confirmation
    * National ID Card master data import by scanning the QR Code

### Changed

* Use `st.experimental_data_editor` instead of `st.dataframe` to show (and alter) dataframes
* Moved `streamlit_image_select` to modules folder

### Fixed

* Changed `@st.experimental_memo` to `@st.cache_data` in module streamlit_image_select to prevent deprecated message
* Added Exception handling for `set_page_config`  error message when it is called more than once
* Added session states for  `st.session_state` has no key "username" error message

## [0.2.0](https://github.com/DrBenjamin/HRStaffPortal/compare/v0.1.1...v0.2.0) - 2023-01-30

``` Pre-Release```

### Added

* HR Staff Portal
    * Images upload via camera
* Statistics Page
* Workshops Page
* Car Fleet Management System
* Handbook Page
* Changelog Page

### Changed

* Custom Tabs instead of build in tabs (extra_streamlit_components)
* Images are cropped and resized

### Fixed

* Simultaneous creating of new employee gives right ID

## [0.1.1](https://github.com/DrBenjamin/HRStaffPortal/compare/v0.1.1...v0.1.1) - 2022-10-18

``` Initial Release```

### Added

* View and edit Employee and training data
* Basic Cloud version with local data stored in csv file (data not persistend)

### Changed

* No changes

### Fixed

* Several logical bugs