$('.auth_container').hover(() => {
    $('.submenu_profile').slideDown();
})

// Отображение трэкинга курса
function showTracking(obj, id) {
    $(obj).attr("class", "fa fa-arrow-circle-up");
    $(obj).attr("title", "Свернуть");
    $(obj).attr("onclick", "").click(() => {
        hideTracking(obj, id)
    });
    $(`#${id}`).show();
}
function hideTracking(obj, id) {
    $(obj).attr("class", "fa fa-arrow-circle-down");
    $(obj).attr("title", "Подробнее");
    $(obj).attr("onclick", "").click(() => {
        showTracking(obj, id)
    });
    $(`#${id}`).hide();
}