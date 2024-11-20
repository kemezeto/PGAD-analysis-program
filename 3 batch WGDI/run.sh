cat Kob.cds >> all.cds
cat Sbr.cds >> all.cds
cat Kob.pep >> all.pep
cat Sbr.pep >> all.pep
wgdi -d total.conf
wgdi -icl total.conf
wgdi -ks total.conf
wgdi -bi total.conf
wgdi -bk total.conf
wgdi -kp total.conf
wgdi -pf total.conf