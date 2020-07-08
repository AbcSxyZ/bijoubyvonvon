
/*
** configureAnchorScroll:
**
** Add an eventListener on the body to give a
** margin whenever the user scroll to an anchor.
*/

function configureAnchorScroll()
{
    var anchorScrolls = {
        ANCHOR_REGEX: /^#[^ ]+$/,
        OFFSET_HEIGHT_PX: 60,

        /**
         * Return the offset amount to deduct from the normal scroll position.
         * Modify as appropriate to allow for dynamic calculations
         */
        getFixedOffset: function() {
            return this.OFFSET_HEIGHT_PX;
        },

        /**
         * If the provided href is an anchor which resolves to an element on the
         * page, scroll to it.
         * @param  {String} href
         * @return {Boolean} - Was the href an anchor.
         */
        scrollIfAnchor: function(href, pushToHistory) {
            var match, rect, anchorOffset;

            if(!this.ANCHOR_REGEX.test(href)) {
                return false;
            }

            match = document.getElementById(href.slice(1));

            if(match) {
                rect = match.getBoundingClientRect();
                anchorOffset = window.pageYOffset + rect.top - this.getFixedOffset();
                window.scrollTo(window.pageXOffset, anchorOffset);
            }

            return !!match;
        },

        /**
         * Attempt to scroll to the current location's hash.
         */
        scrollToCurrent: function() {
            this.scrollIfAnchor(window.location.hash);
        },

        /**
         * If the click event's target was an anchor, fix the scroll position.
         */
        delegateAnchors: function(e) {
            var elem = e.target;

            if(
                elem.nodeName === 'A' &&
                this.scrollIfAnchor(elem.getAttribute('href'), true)
            ) {
                e.preventDefault();
            }
        }
    }
    document.body.addEventListener('click', anchorScrolls.delegateAnchors.bind(anchorScrolls));
};
