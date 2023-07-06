from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .equip_sizes import GloveSize, BatSize
from base_ball_oracle.global_mixins import ValidateParamsMixIn
from parsel import Selector
import requests
from base_ball_oracle.settings import GEAR_SPONSOR
from bb_oracle_apps.web_scraper.web_scrape import WebScraper
# Create your views here.
# https://parsel.readthedocs.io/en/latest/usage.html#examples
# we are getting base64 back we need to extract from scripint..idk if can make that correct if its not in same node tree..how make fixes
# img_url = text.xpath('//div[@class="ArOc1c"]/img').get()
class GloveView(APIView, GloveSize, ValidateParamsMixIn):
    accepted_params = {"age": int.__name__, "position": str.__name__}

    def get(self, request, *args, **kwargs):
        if self.validate_keys(request, "all"):
            self.set_player_level(int(request.query_params["age"]))
            size = self.get_glove_size(request.query_params["position"])
            search_string = self.create_scrape_string(size)
            if search_string is None:
                return Response(
                data={
                    "error": "Invalid Params",
                    "available": self.get_accepted_params(),
                },status=status.HTTP_400_BAD_REQUEST,)
            else:
                scrape_product = WebScraper('https://www.google.com/search', 'https://www.google.com/' ,30,
                                  node_dict={
                                  'product_url':'//div[@class="zLPF4b"]/span["@class=eaGTj mQaFGe shntl"]/div/a/@href',
                                  'product_name':'//div[@class="EI11Pd Hb793d"]/h3[@class="tAxDx"]/text()',
                                  'product_vendor':'//div[@class="aULzUe IuHnof"]/text()',
                                  'product_price':'//div[@class="XrAfOe"]/span/span/span/span[@class="a8Pemb OFFNJ"]/text()',
                                  'product_reviews':'//div[@class="NzUzee"]/div/span[@class="QIrs8"]/text()',
                                  'product_img': '//div[@class="ArOc1c"]/img/@data-image-src',
                                  },
                                  params={
                                   'q':search_string,
                                   'hl':"en",
                                   'gl':"us",
                                   'tbm':"shop",
                                    })
                products = scrape_product.scrape_first_item()
                return Response(
                data={'size':size,'product':products},
                status=status.HTTP_200_OK,
                )
        else:
            return Response(
                data={
                    "error": "Invalid Params",
                    "available": self.get_accepted_params(),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def create_scrape_string(self,size):
        scrape_string = None
        if self.request.query_params["position"] == 'catcher':
            scrape_string = f'{GEAR_SPONSOR} {self.request.query_params["position"]} {size} mitt'
        else:
            scrape_string = f'{GEAR_SPONSOR} {size} baseball glove'
        return scrape_string

class BatView(APIView, BatSize, ValidateParamsMixIn):
    accepted_params = {"height": str.__name__, "weight": int.__name__, "age":int.__name__}

    def get(self, request, *args, **kwargs):
        if self.validate_keys(request, "all"):
            bat = self.get_bat_size(
                int(request.query_params["height"]), int(request.query_params["weight"])
            )
            if bat is None:
                return Response(
                    data={"bat_size": "None Found"}, status=status.HTTP_200_OK
                )
            else:
                drop = self.get_bat_drop(int(request.query_params["age"]))
                scrape_product = WebScraper('https://www.google.com/search', 'https://www.google.com/' ,30,
                                  node_dict={
                                  'product_url':'//div[@class="zLPF4b"]/span["@class=eaGTj mQaFGe shntl"]/div/a/@href',
                                  'product_name':'//div[@class="EI11Pd Hb793d"]/h3[@class="tAxDx"]/text()',
                                  'product_vendor':'//div[@class="aULzUe IuHnof"]/text()',
                                  'product_price':'//div[@class="XrAfOe"]/span/span/span/span[@class="a8Pemb OFFNJ"]/text()',
                                  'product_reviews':'//div[@class="NzUzee"]/div/span[@class="QIrs8"]/text()',
                                  'product_img': '//div[@class="ArOc1c"]/img/@data-image-src',
                                  },
                                  params={
                                   'q':f'{GEAR_SPONSOR} {bat} inch bat {drop} drop',
                                   'hl':"en",
                                   'gl':"us",
                                   'tbm':"shop",
                                    })
                products = scrape_product.scrape_first_item()
                return Response(
                    data={'bat_size':bat,'product':products},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                data={
                    "error": "Invalid Params",
                    "available": self.get_accepted_params(),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
