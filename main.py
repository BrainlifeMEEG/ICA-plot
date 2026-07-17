"""
Visualize ICA components.

This app loads an ICA decomposition object and generates comprehensive visualizations
of the computed independent components, including topographic plots and component properties.

Inputs:
    - ica: Path to ICA decomposition file

Outputs:
    - out_figs/ica.png: Topographic plot of all ICA components
    - out_report/report.html: QC report with component visualizations
    - product.json: Metadata about the visualization
"""

# Copyright (c) 2020 brainlife.io
#
# This app visualizes ICA components

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne
import matplotlib.pyplot as plt

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_figs', 'out_report')

# Load configuration
config = load_config()

# == LOAD ICA OBJECT ==
fname = config['ica']
ica = mne.preprocessing.read_ica(fname, verbose=None)
print(f'Loaded ICA with {ica.n_components} components')

# Initialize product items
product_items = []
add_info_to_product(product_items, f'ICA object loaded with {ica.n_components_} components')

# == PLOT COMPONENTS TOPOGRAPHY ==
plt.figure(figsize=(16, 10))
ica.plot_components(show=False)
components_fig_path = os.path.join('out_figs', 'ica.png')
plt.savefig(components_fig_path, dpi=150)
plt.close()
print(f'Saved component topography plot to {components_fig_path}')

# == CREATE REPORT ==
report = mne.Report(title='ICA Components Visualization')

# Add component information to report
report_html = f'<h3>ICA Decomposition</h3>'
report_html += f'<p><b>Number of Components:</b> {ica.n_components}</p>'
report_html += f'<p><b>Method:</b> {ica.method}</p>'
if hasattr(ica, 'random_state'):
    report_html += f'<p><b>Random State:</b> {ica.random_state}</p>'

report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)
print('Report saved to out_report/report.html')

# == CREATE PRODUCT.JSON ==
add_image_to_product(product_items, 'ICA Components', filepath=components_fig_path)
add_info_to_product(product_items, f'Visualized {ica.n_components_} ICA components', 'success')
create_product_json(product_items)
