"""Generate the main and supplementary vector figures."""
from pathlib import Path
import importlib.util,json,runpy,shutil,sys
M=Path(sys.argv[1]).resolve();DEST=Path(sys.argv[2]).resolve();U=M/'updates'
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(U/'plot'))
for folder in [M/'current/figures/figures',M/'current/figures/qa',U/'figures',U/'revision/qa'] :folder.mkdir(parents=True,exist_ok=True)
sys.argv=[str(U/'plot/plot_current.py'),str(M)]
spec=importlib.util.spec_from_file_location('plot_current',U/'plot/plot_current.py')
plot=importlib.util.module_from_spec(spec);spec.loader.exec_module(plot)
for f in ['protocol','boundary_design','forest','primary','heatmap','state_report','rules','curves','legacy','supplementary_s14','witness_tables']:getattr(plot,f)()
for name in ['draw_axes.py','draw_overview.py']:
    sys.argv=[str(U/'plot'/name),str(M)];runpy.run_path(U/'plot'/name,run_name='__main__')
mapping=json.loads((ROOT/'FIGURE_MAP.json').read_text())
for row in mapping:
    filename=row['generator_file']
    src=(U/'figures' if filename.startswith('v14_') else M/'current/figures/figures')/filename
    assert src.is_file(),src
    dst=DEST/row['document']/row['file'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
assert len(list(DEST.rglob('*.pdf')))==21
print(json.dumps({'passed':True,'main':10,'supplement':11,'note':'Numeric values, layout and current axis conventions are generated from frozen inputs. Font rendering may vary by platform.'}))
