from pathlib import Path
import os
import re

root = Path(__file__).resolve().parents[1]
os.chdir(root)
source = root / 'quantumultx/rewrite/AdBlock-Script.conf'
lines = []
for line in source.read_text(encoding='utf-8-sig').splitlines():
    if 'smzdm' in line and not line.startswith('hostname ='):
        continue
    if line.startswith('hostname ='):
        line = 'hostname = ' + ','.join(h.strip() for h in line.split('=', 1)[1].split(',') if 'smzdm' not in h)
    line = line.replace('https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/script/startup/startup.js', 'https://raw.githubusercontent.com/lester2077/QuantumultX-AdBlock-CN/main/quantumultx/script/splash-killer.js')
    lines.append(line)
text = '\n'.join(lines) + '\n'
count = sum(' url ' in line for line in lines)
text = text.replace('# NAME: AdBlock-Script', '# NAME: AdBlock-Script-a')
text = re.sub(r'^# TOTAL:.*$', f'# TOTAL: {count}', text, flags=re.M)
(root / 'quantumultx/rewrite/AdBlock-Script-a.conf').write_text(text, encoding='utf-8')
from pathlib import Path
root=Path('quantumultx'); out=root/'merged';out.mkdir(exist_ok=True)
inputs=['Splash-Killer.list','BlockHttpDNS.list','AdBlock-Lite.list']
seen=set(); rules=[]
for name in inputs:
 for line in (root/'filter'/name).read_text(encoding='utf-8-sig').splitlines():
  line=line.strip()
  if not line or line.startswith(('#',';')):continue
  key=','.join(x.strip() for x in line.split(','))
  if key not in seen:seen.add(key);rules.append(line)
(out/'AdBlock-Merged.list').write_text('# NAME: AdBlock-Merged\n# Sources: '+', '.join(inputs)+f'\n# TOTAL: {len(rules)}\n\n'+'\n'.join(rules)+'\n',encoding='utf-8')
rewrites=[];hosts=[];seen=set()
for name in ['AdBlock-Splash.conf','AdBlock-Script-a.conf']:
 for line in (root/'rewrite'/name).read_text(encoding='utf-8-sig').splitlines():
  line=line.strip()
  if not line or line.startswith(('#',';')):continue
  if line.startswith('hostname ='):
   hosts.extend(x.strip() for x in line.split('=',1)[1].split(','));continue
  if line not in seen:seen.add(line);rewrites.append(line)
script_patterns={line.split(' url ',1)[0] for line in rewrites if ' url script-' in line}
removed=[line for line in rewrites if ' url reject' in line and line.split(' url ',1)[0] in script_patterns]
rewrites=[line for line in rewrites if line not in removed]
# Keep response script declarations before remaining static rewrites.
rewrites.sort(key=lambda line:0 if ' url script-' in line else 1)
(out/'AdBlock-Merged.conf').write_text('# NAME: AdBlock-Merged\n# Sources: AdBlock-Splash.conf, AdBlock-Script-a.conf\n'+f'# TOTAL: {len(rewrites)}\n\n'+'\n'.join(rewrites)+'\nhostname = '+','.join(dict.fromkeys(hosts))+'\n',encoding='utf-8')
(out/'README.md').write_text('''# 合并规则

- AdBlock-Merged.list：合并 Splash-Killer.list、BlockHttpDNS.list、AdBlock-Lite.list，按完整规则去重，保留原顺序和策略。
- AdBlock-Merged.conf：合并 AdBlock-Splash.conf、AdBlock-Script-a.conf，合并 hostname；完全相同 URL 正则的拒绝规则让位于脚本，脚本声明放在前面。

list 用于分流规则，conf 用于 MITM 模块。不要同时启用其原始来源，避免重复规则。

注意：未将域名 REJECT 自动改为放行。域名拦截或较宽的重写拦截仍可能导致响应脚本拿不到服务器响应；按具体 App 的请求日志排查。脚本仍使用远程地址，需下载成功并启用模块与 MITM，证书需正确配置。未进行客户端流量实测。
''',encoding='utf-8')
assert len(rules) == len(set(rules))
assert len(rewrites)==len(set(rewrites))
assert all(not (' url reject' in x and x.split(' url ',1)[0] in script_patterns) for x in rewrites)
print(f'Routing: {len(rules)}; rewrite: {len(rewrites)}; exact reject conflicts removed: {len(removed)}; hosts: {len(set(hosts))}')
for line in removed:print('Removed: '+line)
