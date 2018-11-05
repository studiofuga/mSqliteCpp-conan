#include <iostream>
#include <msqlitecpp/sqlitestorage.h>

int main() {
    sqlite::sqlitestorage s(":memory:");
    return 0;
}
