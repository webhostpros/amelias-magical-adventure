"""Scan only explicitly tracked publication files, without displaying secret values."""
import json,re,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
files=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0');files=[x for x in files if x]
patterns={
 'github_token':rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})',
 'openai_key':rb'sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{35,}',
 'aws_access_key':rb'AKIA[0-9A-Z]{16}',
 'private_key':rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
 'credential_assignment':rb'(?i)(?:api[_-]?key|password|client[_-]?secret|access[_-]?token)\s*[=:]\s*[\"\x27]?[A-Za-z0-9_+/-]{20,}'
}
findings=[];oversized=[];unwanted=[]
for name in files:
 p=root/name
 if p.stat().st_size>=100_000_000:oversized.append(name)
 if any(x in name.lower().split('/') for x in ['saved','intermediate','deriveddatacache','docs-no-upload','fab','animals_free','medieval_castle']):unwanted.append(name)
 data=p.read_bytes()
 for label,pattern in patterns.items():
  if re.search(pattern,data) or re.search(pattern,data.replace(b'\x00',b'')):findings.append({'path':name,'rule':label})
report={'tracked_files':len(files),'secret_findings':findings,'oversized_files':oversized,'excluded_source_violations':unwanted}
print(json.dumps(report,indent=2));sys.exit(bool(findings or oversized or unwanted))
