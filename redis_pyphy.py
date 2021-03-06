import pyphy
import redis
import subprocess

#### start the redis server
import os
devnull = open(os.devnull, 'w')

p = subprocess.Popen(["redis-server"], stdout=devnull, stderr=devnull)

#os.system("redis-server")

cache = redis.StrictRedis(charset="utf-8", decode_responses=True)

import psutil
from multiprocessing import Pool
import sys


input_file = sys.argv[1]

list_of_query = []

desired_ranks = ["superkingdom", "phylum", "class", "order", "family", "genus", "species"]

num_of_cpu = psutil.cpu_count()
evalue_cutoff = 1e-10

with open(input_file) as input:

    previous_query = ""

    one_query = []

    for line in input:
        fields = line.strip().split("\t")

        taxid = fields[-1].split(";")[0]
        evalue = fields[-4]
        query_name = fields[0]
        score = fields[-3]
        pident = fields[2]
        qcovs = fields[3]

        #print (query_name, taxid, score, pident, qcovs)

        if float(evalue) < evalue_cutoff:
            if previous_query != query_name:
                previous_query = query_name

                #list_of_query.append([query, taxid, score, pident, qcovs])
                if len(one_query) != 0:
                    list_of_query.append(one_query)

                one_query = []
                one_query.append([query_name, taxid, score, pident, qcovs, evalue])
            
            else:
                one_query.append([query_name, taxid, score, pident, qcovs, evalue])

    if len(one_query) != 0:
        list_of_query.append(one_query)

def worker(one_query):
    #print (taxid)

    name_path = {}
    query_name = ""

    #print (one_query)

    for query in one_query:

        if len(name_path) == 0:

            query_name, taxid, score, pident, qcovs, evalue = query

            temp_name_path = {}

            if cache.exists(taxid):
                temp_name_path = cache.hgetall(taxid)
            else:
                
                path = pyphy.getDictPathByTaxid(taxid)

                temp_name_path = {rank: pyphy.getNameByTaxid(path[rank]) for rank in path}

                cache.hmset(taxid, temp_name_path)

            if "phylum" in temp_name_path:
                name_path = temp_name_path

    if len(name_path) != 0:
        content = "\t".join([query_name, taxid, score, pident, qcovs, evalue]) + "\t"
        for rank in desired_ranks:
            if rank in name_path:
                content += name_path[rank] + "\t"
            else:
                content += "\t"
        
        print (content.strip())

#print (list_of_query)

with Pool(num_of_cpu) as P:
    P.map(worker, list_of_query)



cache.flushdb()

p = subprocess.Popen(["killall", "redis-server"], stdout=devnull, stderr=devnull)