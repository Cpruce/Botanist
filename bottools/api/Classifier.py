#!/usr/bin/python
#
#   File created by Cory Pruce on 10/25/2015
#
#   Part of the RevEngdroid project
#
#
#   The classifier program takes a signature and compares against previously
#   seen instances through clusters. If the distance is within a certain
#   threshold, the signature is added to the cluster. If it does not fall within
#   the limit distance for a cluster, a new one is created with itself as the
#   cluster id.
#

# Tapered Levenshtein for mnemonic signatures
def tapered_levenshtein(sig1, sig2):
    sig1_mnemonics = sig1
    sig2_mnemonics = sig2
    position = 0
    if len(sig1_mnemonics) < len(sig2_mnemonics):
        num_mnemonics = len(sig1_mnemonics)  
    else: 
        num_mnemonics = len(sig2_mnemonics)
                    # assumption len(sig1) == len(sig2)

    weight = 1.0 - position/num_mnemonics
    distance = 0.0

    for mn1, mn2 in zip(sig1_mnemonics, sig2_mnemonics):
        if mn1 != mn2:
            distance+=weight

        position+=1
        weight = 1.0 - position/num_mnemonics

    return (distance, num_mnemonics)


