/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
define([
    'jquery',
    'mage/translate'
], function ($, $t) {
    'use strict';

    return function (config) {
        var $form = $('#attribute-import-form'),
            $attribute = $('#attribute_code'),
            $file = $('#import_file'),
            $checkButton = $('#check-data-button'),
            $importButton = $('#import-button'),
            $notification = $('#import-notification'),
            $heading = $('#validation-heading'),
            $preview = $('#preview-container'),
            busy = false;

        /**
         * @param {*} text
         * @returns {String}
         */
        function escapeHtml(text) {
            return $('<div>').text(String(text)).html();
        }

        /**
         * @param {String[]|String} messages
         * @returns {String}
         */
        function toHtml(messages) {
            return ($.isArray(messages) ? messages : [messages]).map(escapeHtml).join('<br>');
        }

        /**
         * @param {String} safeHtml
         * @param {String} type 'success' or 'error'
         */
        function showMessage(safeHtml, type) {
            $notification
                .removeClass('hidden message-error message-success')
                .addClass('message ' + (type === 'success' ? 'message-success' : 'message-error'))
                .html($('<div>').html(safeHtml));
        }

        function hideMessage() {
            $notification.addClass('hidden').removeClass('message message-error message-success').empty();
        }

        /**
         * @param {Boolean} importAllowed
         */
        function setButtons(importAllowed) {
            $importButton.prop('disabled', !importAllowed).toggleClass('disabled', !importAllowed);
            $checkButton.prop('disabled', false).removeClass('disabled');
        }

        function resetState() {
            setButtons(false);
            $heading.addClass('hidden');
            $preview.empty();
            hideMessage();
        }

        /**
         * Post the form; buttons stay disabled until the request completes so
         * a double click can never start two imports.
         *
         * @param {String} url
         * @returns {jQuery.Deferred}
         */
        function post(url) {
            busy = true;
            $checkButton.add($importButton).prop('disabled', true).addClass('disabled');

            return $.ajax({
                url: url,
                type: 'POST',
                data: new FormData($form[0]),
                contentType: false,
                processData: false,
                showLoader: true,
                dataType: 'json'
            }).fail(function () {
                setButtons(false);
                showMessage(escapeHtml($t('Server error. Please try again.')), 'error');
            }).always(function () {
                busy = false;
            });
        }

        function checkData() {
            if (busy) {
                return;
            }
            post(config.previewUrl).done(function (response) {
                if (!response.success) {
                    setButtons(false);
                    showMessage(escapeHtml(response.message || $t('Server error. Please try again.')), 'error');

                    return;
                }

                // Server-rendered preview: every cell is escaped in preview.phtml.
                $preview.html(response.data);
                $heading.removeClass('hidden');

                if (response.is_valid) {
                    hideMessage();
                    setButtons(true);
                } else {
                    setButtons(false);
                    showMessage(escapeHtml($t('Validation failed. Please fix the errors shown below.')), 'error');
                }
            });
        }

        function runImport() {
            if (busy || $importButton.prop('disabled')) {
                return;
            }
            post(config.processUrl).done(function (response) {
                var html = toHtml(response.messages || []);

                if (response.success && response.skipped > 0) {
                    html += '<br><em>' + escapeHtml(
                        $t('%1 option(s) skipped (already exist). See log for details.').replace('%1', response.skipped)
                    ) + '</em>';
                }

                resetState();
                $file.val('');
                $attribute.prop('selectedIndex', 0);
                showMessage(html, response.success ? 'success' : 'error');
            });
        }

        $attribute.add($file).on('change', resetState);
        $checkButton.on('click', checkData);
        $importButton.on('click', runImport);
        $('#view-log-button').on('click', function () {
            window.location.href = config.logUrl;
        });

        resetState();
    };
});
