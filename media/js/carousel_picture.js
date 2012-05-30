function carouselShape_initCallback(carousel)
	        {
           carousel.buttonNext.bind('click', function()
            {
                carousel.startAuto(0);
            });
          carousel.buttonPrev.bind('click', function()
           {
	                carousel.startAuto(0);
	            });
	            carousel.clip.hover(function()
	            {
	                carousel.stopAuto();
	            }, function()
	            {
	                carousel.startAuto();
	            });
	        };
        jQuery(document).ready(function()
	        {
	            jQuery('#hotsharing-carousel').jcarousel(
           {
	            auto: 0,
                wrap: "both",
                scroll: 1, 
                initCallback: carouselShape_initCallback
                
            });
            jQuery('#followed-sharings-carousel').jcarousel();
            jQuery('#secondaaa').jcarousel();
        });