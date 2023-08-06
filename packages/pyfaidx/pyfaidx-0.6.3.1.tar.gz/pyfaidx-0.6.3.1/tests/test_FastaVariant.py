import os
from pyfaidx import FastaVariant, Fasta
from unittest import TestCase
from nose.plugins.skip import SkipTest


path = os.path.dirname(__file__)
os.chdir(path)

class TestFastaVariant(TestCase):
    
    def setUp(self):
        pass
        # raise SkipTest

    def tearDown(self):
        try:
            os.remove('data/chr22.fasta.fai')
        except EnvironmentError:
            pass  # some tests may delete this file

    def test_fetch_variant(self):
        try:
            import pysam
            fasta = FastaVariant('data/chr22.fasta', 'data/chr22.vcf.gz', hom=True, het=True, as_raw=True)
            assert fasta['22'][32330458:32330462] == 'CAGG'  # het
            assert fasta['22'][32352282:32352286] == 'CAGC'  # hom
        except (ImportError, IOError):
            raise SkipTest

    def test_fetch_hom_variant(self):
        try:
            import pysam
            fasta = FastaVariant('data/chr22.fasta', 'data/chr22.vcf.gz', hom=True, het=False, as_raw=True)
            assert fasta['22'][32330458:32330462] == 'CGGG'  # het
            assert fasta['22'][32352282:32352286] == 'CAGC'  # hom
        except (ImportError, IOError):
            raise SkipTest

    def test_fetch_het_variant(self):
        try:
            import pysam
            fasta = FastaVariant('data/chr22.fasta', 'data/chr22.vcf.gz', hom=False, het=True, as_raw=True)
            assert fasta['22'][32330458:32330462] == 'CAGG'  # het
            assert fasta['22'][32352282:32352286] == 'CGGC'  # hom
        except (ImportError, IOError):
            raise SkipTest

    def test_fetch_chr_not_in_vcf(self):
        try:
            import pysam
            fasta = FastaVariant('data/chr22andfake.fasta', 'data/chr22.vcf.gz', hom=True, het=True, as_raw=True)
            assert fasta['fake'][:10] == 'ATCG' # fake is not in vcf 
        except (ImportError, IOError):
            raise SkipTest
        
    def test_all_pos(self):
        try:
            import pysam
            fasta = FastaVariant('data/chr22.fasta', 'data/chr22.vcf.gz', hom=True, het=True, as_raw=True)
            assert fasta['22'].variant_sites == (16042793, 21833121, 29153196, 29187373, 29187448, 29194610, 29821295, 29821332, 29993842, 32330460, 32352284)
        except (ImportError, IOError):
            raise SkipTest

    def test_all_diff(self):
        try:
            fasta = FastaVariant('data/chr22.fasta', 'data/chr22.vcf.gz', hom=True, het=True, as_raw=True)
            ref = Fasta('data/chr22.fasta', as_raw=True)
            print([(ref['22'][pos-1], fasta['22'][pos-1]) for pos in fasta['22'].variant_sites])
            assert all(ref['22'][pos-1] != fasta['22'][pos-1] for pos in fasta['22'].variant_sites)
        except (ImportError, IOError):
            raise SkipTest
